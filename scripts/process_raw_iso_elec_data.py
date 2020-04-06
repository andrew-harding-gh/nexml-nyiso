"""
this script assumes the raw archive data is available for aggregation, and then produces
local csv files with that aggregation
"""

import glob
import pandas as pd

from plumbum import local
from zipfile import ZipFile


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
                    df['source_file_name'] = csv_file.filename
                    df.to_csv(path_or_buf=str(master_file), mode='a', header=first, index=False)
                    first = False


if __name__ == '__main__':
    create_master_elec_csv_from_raw_data('pal')
    create_master_elec_csv_from_raw_data('isolf')
