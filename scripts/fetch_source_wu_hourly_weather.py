"""
This is simple (and brittle) data scraper that fetches all hourly time-series data over a period of time
from WeatherUnderground's store of historical weather.
To use, one should retrieve an api key by inspecting a browser's network requests.
Data is dumped locally to .csv files
"""

import json
import requests
import time

import pandas as pd
from dateutil.relativedelta import relativedelta
from plumbum import local

from nexml_nyiso.notebooks.utils import START_DATE, END_DATE

pd.options.mode.chained_assignment = None  # default='warn'


class WuApiScraper:
    def __init__(self, key, start, end):
        self.key = key
        self.start_date = start
        self.end_date = end

    def dump_to_file(self, dt_obj, station, records):
        dir_ = local.path(__file__).dirname
        new = local.path(dir_ / 'downloads' / 'hourly')
        if not new.exists():
            new.mkdir()
        fn = local.path(new / f'{station}_hourly_weather_{dt_obj.year}_{dt_obj.month}.csv')

        df = pd.DataFrame.from_records(records)

        df.to_csv(str(fn), index=False)
        print(f'data written for {str(dt_obj.date())}.')

    def main(self, station):

        cur_date = self.start_date
        fmt_ = "%Y%m%d"

        while cur_date <= self.end_date:
            print(f'fetching data for {cur_date.year}-{cur_date.month}-{cur_date.day}')

            month_end = cur_date + relativedelta(months=1) - relativedelta(days=1)
            local_start = cur_date.strftime(fmt_)
            local_end = month_end.strftime(fmt_)

            url = f'https://api.weather.com/v1/location/{station}:9:US/observations/historical.json?' \
                  f'apiKey={self.key}&units=e&startDate={local_start}&endDate={local_end}'
            r = requests.get(url)

            if not r.status_code == 200:
                raise Exception(f'request failed with key {self.key} for URL {url}')

            d = json.loads(r.text)
            data = d['observations']

            self.dump_to_file(cur_date, station, data)

            time.sleep(3)
            cur_date += relativedelta(months=1)

        print('data fetched successfully')


if __name__ == '__main__':
    """
     Nothing special about this api key, simply filched from a browser request.
     New one can be fetched by accessing site in browser eg (https://www.wunderground.com/history/daily/KLGA/date/2017-5-5) 
     and checking networks calls to `api.weather.com`
    """
    w = WuApiScraper(
        key="6532d6454b8aa370768e63d6ba5a832e",
        start=START_DATE,
        end=END_DATE
    )
    w.main('KJFK')
    w.main('KLGA')
