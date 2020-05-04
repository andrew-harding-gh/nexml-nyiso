import re

import pandas as pd
from plumbum import local

zipped = False
pattern = re.compile(r".*hourly_weather.*\.csv")

dir_ = local.path(__file__).dirname
dl_dir = dir_ / 'downloads' / 'hourly'

df = pd.DataFrame()

for csv in dl_dir.walk(filter=lambda x: re.match(pattern, x)):
    in_df = pd.read_csv(str(csv))
    df = pd.concat([df, in_df])

df.sort_values(by=['valid_time_gmt'], inplace=True)

fn = local.path(__file__).dirname.up() / 'data' / 'klga_hourly_weather_historicals'
if zipped:
    df.to_csv(str(fn.with_suffix('.gz')), index=False, compression='gzip')
else:
    df.to_csv(str(fn.with_suffix('.csv')), index=False)
