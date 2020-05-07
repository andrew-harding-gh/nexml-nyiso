"""
This script processes and aggregates

"""

import re
from datetime import datetime

import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
from plumbum import local
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from zipfile import ZipFile

from nexml_nyiso.notebooks.utils import START_DATE, END_DATE

pd.options.mode.chained_assignment = None  # default='warn'


def aggregate_files(from_archive):
    pattern = re.compile(r".*hourly_weather.*\.csv")
    dir_ = local.path(__file__).dirname

    df = pd.DataFrame()

    if not from_archive:
        dl_dir = dir_ / 'downloads' / 'hourly'

        for csv in dl_dir.walk(filter=lambda x: re.match(pattern, x)):
            in_df = pd.read_csv(str(csv))
            df = pd.concat([df, in_df])

    else:
        zip_path = local.path(__file__).dirname.up() / 'raw_data' / 'wu_archive' / 'hourly.zip'
        zf = ZipFile(str(zip_path))
        for csv_file in zf.filelist:
            with zf.open(csv_file.filename) as csv:
                in_df = pd.read_csv(csv)
                df = pd.concat([df, in_df])

    df.sort_values(by=['valid_time_gmt'], inplace=True)
    df.reset_index(inplace=True)

    return df


def clean_df(df):
    """ ! modifiies df in place """

    header_map = {
        'valid_time_gmt': 'datetime',
        'temp': 'temp',
        'dewPt': 'dwpt',
        'rh': 'rh',
        'wspd': 'wspd',
        'wdir': 'wdir',
        'wc': 'wc',
        'pressure': 'pressure',
        'precip_hrly': 'prcp',
        'clds': 'clds',
        'uv_index': 'uv_idx',
        'feels_like': 't_app',
        'vis': 'vis',
        'heat_index': 'heat_idx'
    }
    df.rename(columns=header_map, inplace=True)

    df.drop(list(set(df.columns) - set(header_map.values())), axis=1, inplace=True)
    df[header_map['valid_time_gmt']] = \
        df[header_map['valid_time_gmt']].apply(lambda x: datetime.fromtimestamp(x))

    # only select data that is on "official" timeline ie. %h:51:00
    df = df.loc[df[header_map['valid_time_gmt']].dt.minute == 51]
    df.drop_duplicates(subset=header_map['valid_time_gmt'], inplace=True)

    # then just bump it up to closest hour
    df[header_map['valid_time_gmt']] = \
        df[header_map['valid_time_gmt']].apply(lambda x: x + relativedelta(minutes=9))

    # now handle missing vals
    df = handle_missing_values(df)

    return df


def handle_missing_values(df):
    """
    Parameters
    ----------
    df: expects dataframe with renamed columns

    Returns df
    -------

    """
    # precip
    df.prcp.fillna(0, inplace=True)

    # wind
    df.wdir.fillna(method='ffill', inplace=True)  # forward fill direction when missing and when Null due to do wind
    df.wspd.fillna(0, inplace=True)

    # # dew point
    # # try to calc first, if not missing data, just interpolate
    #
    # df[df.dwpt.isnull()].dwpt = \
    #     df[df.dwpt.isnull()].apply(lambda row: calc_dwpt(row.temp, row.rh) if (np.all(pd.notnull([row.rh, row.temp]))) else row, axis=1)

    df.interpolate(method='nearest', inplace=True)
    df.clds.fillna('CLR', inplace=True)  # categorical fill
    # i've only checked the most consecutive missing for dwpt and it was 13, see below for how to
    # df.COL.isnull().astype(int).groupby(df.COL.notnull().astype(int).cumsum()).sum().max()

    return df


def calc_dwpt(temp, rh):
    """
    temp: assume temp is in F --> float;
    rh: relative humidity --> float;
    """
    # first convert to celcius
    temp = (temp - 32) * 5 / 9
    return round(
        243.04 * (np.log(rh / 100) + ((17.625 * temp) / (243.04 + temp))) / (
                17.625 - np.log(rh / 100) - ((17.625 * temp) / (243.04 + temp))),
        1
    )


def output_df(df):
    fn = local.path(__file__).dirname.up() / 'data' / 'klga_hourly_weather_historicals'
    df.to_csv(str(fn.with_suffix('.csv')), index=False)


def main(from_archive):
    df = aggregate_files(from_archive)
    df = clean_df(df)
    output_df(df)


if __name__ == '__main__':
    FROM_ARCHIVE = True  # if processing the repo-archived files in `raw_data`
    print(f'Beginning weather underground file aggregation...')
    main(FROM_ARCHIVE)
