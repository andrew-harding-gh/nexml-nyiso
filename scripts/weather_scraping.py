import time
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta

import pandas as pd
from selenium import webdriver
from plumbum import local
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from nexml_nyiso.notebooks.utils import START_DATE, END_DATE

CHROMEDRIVER_PATH = "../chromedriver"
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')


class WeatherScraper:
    def __init__(self):
        self.webdriver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=chrome_options)
        self.station = "KLGA"
        self.base_url = f"https://www.wunderground.com/"

    def quit(self):
        self.webdriver.close()

    def main(self):
        cur_date = START_DATE
        while cur_date <= END_DATE:
            print(f'fetching data for {cur_date.year}-{cur_date.month}')
            self.get_month_history(cur_date.year, cur_date.month)
            time.sleep(5)
            cur_date += relativedelta(months=1)

        print('------ ~~ all dates output ~~ ------')
        self.webdriver.quit()

    def get_month_history(self, year, month):
        url = self.base_url + f'history/monthly/{self.station}/date/{year}-{month}'
        self.webdriver.get(url)

        time.sleep(5)
        wait = WebDriverWait(self.webdriver, 30)
        table = wait.until(
            EC.presence_of_element_located(
                (By.XPATH,
                 "/html/body/app-root/app-history/one-column-layout/wu-header/sidenav/mat-sidenav-container/mat-sidenav-content/div/section/div[2]/div[1]/div[5]/div[1]/div/lib-city-history-observation/div/div[2]/table")
            )
        )

        self.parse_observation_table(table, year, month)

    def parse_observation_table(self, table, year, month):
        """
        HEADERS = ['Date', 'Temperature (°F)', 'Dew Point (°F)', 'Humidity (%)', 'Wind Speed (mph)', 'Pressure (Hg)', 'Precipitation (in)']
        """
        HEADERS = ['date', 't', 'dwpt', 'rh', 'ws', 'pr', 'prcp']
        body = table.find_element_by_tag_name('tbody')
        raw_dfs = pd.read_html(body.get_attribute('innerHTML'))
        processed_dfs = list()

        for i, df in enumerate(raw_dfs):
            if i == 0:
                processed_dfs.append(self.process_date_df(df, year, month, HEADERS[i]))
            else:
                # pop first row to col header
                df.columns = [f"{HEADERS[i]}_{x.lower()}" for x in df.iloc[0]]
                processed_dfs.append(df[1:])

        out = pd.concat(processed_dfs, axis=1, sort=False)
        self.dump_to_file(year, month, out)

    def process_date_df(self, df, year, month, header):
        """ build the date col """
        df.columns = [header]
        df = df[1:]
        df[header] = df[header].apply(lambda x: datetime(year, month, int(x)).date())
        return df

    def dump_to_file(self, year, month, df):
        dir_ = local.path(__file__).dirname
        new = local.path(dir_ / 'downloads' / 'daily')
        if not new.exists():
            new.mkdir()
        fn = local.path(new / f'{self.station.lower()}_weather_{str(year)}_{str(month)}.csv')

        df.to_csv(str(fn), index=False)
        print('data written for date.')


class CombineWeatherHistorical:

    def __init__(self, zipped=False):
        self.zipped = zipped

    def main(self):
        pattern = re.compile(r".*weather.*\.csv")

        dir_ = local.path(__file__).dirname
        dl_dir = dir_ / 'downloads' / 'daily'

        df = pd.DataFrame()

        for csv in dl_dir.walk(filter=lambda x: re.match(pattern, x)):
            in_df = pd.read_csv(str(csv))
            df = pd.concat([df, in_df])

        df.sort_values(by=['date'], inplace=True)

        fn = local.path(__file__).dirname.up() / 'data' / 'klga_weather_historicals'
        if self.zipped:
            df.to_csv(str(fn.with_suffix('.gz')), index=False, compression='gzip')
        else:
            df.to_csv(str(fn.with_suffix('.csv')), index=False)


if __name__ == '__main__':
    WeatherScraper().main()
    CombineWeatherHistorical().main()
