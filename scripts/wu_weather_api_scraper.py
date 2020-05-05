"""
This is simple (and brittle) data scraper that fetches all hourly time-series data over a period of time
from WeatherUnderground's store of historical weather.
To use, one should retrieve an api key by inspecting a browser's network requests.
Files are grouped by month and eventually aggregated to one single .csv or .gzip
"""

import json
import re
import requests
import time
from datetime import datetime

import pandas as pd
from dateutil.relativedelta import relativedelta
from plumbum import local

from nexml_nyiso.notebooks.utils import START_DATE, END_DATE

pd.options.mode.chained_assignment = None  # default='warn'


class WuApiScraper:
    def __init__(self, key, station, start, end):
        self.key = key
        self.station = station
        self.start_date = start
        self.end_date = end

    def dump_to_file(self, dt_obj, records):
        dir_ = local.path(__file__).dirname
        new = local.path(dir_ / 'downloads' / 'hourly')
        if not new.exists():
            new.mkdir()
        fn = local.path(new / f'{self.station}_hourly_weather_{dt_obj.year}_{dt_obj.month}.csv')

        df = pd.DataFrame.from_records(records)

        df.to_csv(str(fn), index=False)
        print(f'data written for {str(dt_obj.date())}.')

    @staticmethod
    def aggregate_files():
        pattern = re.compile(r".*hourly_weather.*\.csv")

        dir_ = local.path(__file__).dirname
        dl_dir = dir_ / 'downloads' / 'hourly'

        df = pd.DataFrame()

        for csv in dl_dir.walk(filter=lambda x: re.match(pattern, x)):
            in_df = pd.read_csv(str(csv))
            df = pd.concat([df, in_df])

        df.sort_values(by=['valid_time_gmt'], inplace=True)
        df.reset_index(inplace=True)
        return df

    @staticmethod
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

        # precip
        df[header_map['precip_hrly']].fillna(0, inplace=True)

        # # wind
        # df[df[header_map['wspd']].isnull()][header_map['wdir']].fillna(0, inplace=True)
        # df[header_map['wspd']].fillna(0, inplace=True)

        return df

    def output_df(self, df, zipped=False):
        fn = local.path(__file__).dirname.up() / 'data' / f'{self.station}_hourly_weather_historicals'
        if zipped:
            df.to_csv(str(fn.with_suffix('.gz')), index=False, compression='gzip')
        else:
            df.to_csv(str(fn.with_suffix('.csv')), index=False)

    def main(self):

        cur_date = self.start_date
        fmt_ = "%Y%m%d"

        while cur_date <= self.end_date:
            print(f'fetching data for {cur_date.year}-{cur_date.month}-{cur_date.day}')

            month_end = cur_date + relativedelta(months=1) - relativedelta(days=1)
            local_start = cur_date.strftime(fmt_)
            local_end = month_end.strftime(fmt_)

            url = f'https://api.weather.com/v1/location/{self.station}:9:US/observations/historical.json?' \
                  f'apiKey={self.key}&units=e&startDate={local_start}&endDate={local_end}'
            r = requests.get(url)

            if not r.status_code == 200:
                raise Exception(f'request failed with key {self.key} for URL {url}')

            d = json.loads(r.text)
            data = d['observations']

            self.dump_to_file(cur_date, data)

            time.sleep(3)
            cur_date += relativedelta(months=1)

        print('data fetched successfully')
        print('Aggregating csvs')
        raw = self.aggregate_files()
        clean = self.clean_df(raw)
        self.output_df(clean)
        self.aggregate_files()
        print('we done')


if __name__ == '__main__':
    """
     Nothing special about this api key, simply filched from a browser request.
     New one can be fetched by accessing site in browser eg (https://www.wunderground.com/history/daily/KLGA/date/2017-5-5) 
     and checking networks calls to `api.weather.com`
    """
    w = WuApiScraper(
        key="6532d6454b8aa370768e63d6ba5a832e",
        station='KLGA',
        start=START_DATE,
        end=END_DATE
    )
    w.main()
