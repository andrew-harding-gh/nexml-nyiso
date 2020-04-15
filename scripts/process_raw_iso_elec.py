"""
this script assumes the raw archive data is available for aggregation, and then produces
local csv files with that aggregation
"""

import datetime
import glob
import pandas as pd

from plumbum import local
from zipfile import ZipFile

pd.options.mode.chained_assignment = None  # default='warn'

NYC_PTID = 61761


def wrangle_isolf_data(df):
    """
    ! mutates df in place

    Returns: single row df describing the predicted daily load
    """
    df = df[['Time Stamp', 'N.Y.C.', 'file_date']]
    df['Time Stamp'] = df['Time Stamp'].apply(lambda x: datetime.datetime.strptime(x, '%m/%d/%Y %H:%M').date())
    df = df.loc[df['Time Stamp'] == df['file_date']]
    df['min'], df['max'], df['mean'] = df['N.Y.C.'].agg(['min', 'max', 'mean'])

    df = df.tail(n=1)
    df['Name'] = 'N.Y.C.'
    df['PTID'] = NYC_PTID
    df.drop(['N.Y.C.', 'file_date'], axis='columns', inplace=True)
    return df.reset_index(drop=True)


def wrangle_pal_data(df):
    """
     ! mutates pal df in place

     Returns: single row df with info about daily load
    """
    # drop anything not specifically the NYC region (this drop includes NYC_LI region in early records)
    df = df.loc[df['PTID'] == NYC_PTID]

    df['Time Stamp'] = df['Time Stamp'].apply(lambda x: datetime.datetime.strptime(x, '%m/%d/%Y %H:%M:%S').date())

    df['min'], df['max'], df['mean'] = df['Load'].agg(['min', 'max', 'mean'])
    df.drop(['Time Zone', 'Load'], axis='columns', inplace=True)
    return df.tail(n=1).reset_index(drop=True)


def create_master_elec_csv_from_raw_data(archive_name):
    master_file = local.path(__file__).dirname.up() / 'data' / f'nyiso_{archive_name}_master.csv'

    if master_file.exists():
        new = master_file.dirname / f'nyiso_{archive_name}_master_NEW.csv'
        if new.exists():
            new.delete()
        new.touch()
        master_file = new
    else:
        master_file.touch()

    file_names = glob.glob(f'../raw_data/{archive_name}_archive/*.zip')
    first = True  # get headers from the first csv, then ignore the rest

    for file in file_names:
        with ZipFile(file) as myzip:
            for csv_file in myzip.filelist:
                with myzip.open(csv_file.filename) as csv:
                    df = pd.read_csv(csv)

                    if archive_name == 'pal':
                        df = wrangle_pal_data(df)
                    elif archive_name == 'isolf':
                        df['file_date'] = datetime.datetime.strptime(csv_file.filename[:8], "%Y%m%d").date()
                        df = wrangle_isolf_data(df)

                    df.to_csv(path_or_buf=str(master_file), mode='a', header=first, index=False)
                    first = False


if __name__ == '__main__':
    print('Beginning file aggregation...')
    create_master_elec_csv_from_raw_data('pal')
    print('Actual load (PAL) agg completed.')
    create_master_elec_csv_from_raw_data('isolf')
    print('ISO Load Forecasts (ISOLF) agg completed.')
