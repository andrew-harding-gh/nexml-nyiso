"""
This script processes and aggregates

"""

import re
from datetime import datetime

import pandas as pd
from dateutil.relativedelta import relativedelta
from plumbum import local
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
    # no precrp is recorded without a value
    df.prcp.fillna(0, inplace=True)

    # forward fill direction when missing and when Null due to do wind
    df.wdir.fillna(method='ffill', inplace=True)
    df.wspd.fillna(0, inplace=True)

    df.interpolate(method='nearest', inplace=True)
    df.clds.fillna('CLR', inplace=True)  # categorical fill

    return df


def output_df(df, station):
    fn = local.path(__file__).dirname.up() / 'data' / f'{str(station)}_hourly_weather_historicals'
    df.to_csv(str(fn.with_suffix('.csv')), index=False)


def main(from_archive, station):
    df = aggregate_files(from_archive)
    df = clean_df(df)
    output_df(df, station)


if __name__ == '__main__':
    FROM_ARCHIVE = True  # if processing the repo-archived files in `raw_data`
    STATION = 'JFK'
    print(f'Beginning weather underground file aggregation...')
    main(FROM_ARCHIVE, STATION)
