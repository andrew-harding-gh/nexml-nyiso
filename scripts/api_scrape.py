import requests
import json
import time

import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

from plumbum import local

from nexml_nyiso.notebooks.utils import START_DATE, END_DATE


def dump_to_file(dt_obj, records):
    dir_ = local.path(__file__).dirname
    new = local.path(dir_ / 'downloads' / 'hourly')
    if not new.exists():
        new.mkdir()
    fn = local.path(new / f'KLGA_hourly_weather_{dt_obj.year}_{dt_obj.month}_{dt_obj.day}.csv')

    df = pd.DataFrame.from_records(records)

    df.to_csv(str(fn), index=False)
    print(f'data written for {str(dt_obj.date())}.')

START_DATE = datetime(2008, 10, 7)  # manually ended scrape here
cur_date = START_DATE

while cur_date <= END_DATE:
    print(f'fetching data for {cur_date.year}-{cur_date.month}-{cur_date.day}')

    key = "6532d6454b8aa370768e63d6ba5a832e"
    date = cur_date.strftime("%Y%m%d")
    url = f'https://api.weather.com/v1/location/KLGA:9:US/observations/historical.json?apiKey={key}&units=e&startDate={date}'
    r = requests.get(url)

    if not r.status_code == 200:
        raise Exception(f'request failed with key {key} for URL {url}')

    d = json.loads(r.text)
    data = d['observations']

    dump_to_file(cur_date, data)

    time.sleep(3)
    cur_date += relativedelta(days=1)


print('we done')