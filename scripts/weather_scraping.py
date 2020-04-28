import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import pandas as pd
from selenium import webdriver
from plumbum import local
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from notebooks.utils import START_DATE, END_DATE

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

        # TODO: proper wait for load
        time.sleep(5)

        table = self.webdriver.find_element_by_xpath(
            "/html/body/app-root/app-history/one-column-layout/wu-header/sidenav/mat-sidenav-container/mat-sidenav-content/div/section/div[2]/div[1]/div[5]/div[1]/div/lib-city-history-observation/div/div[2]/table")

        self.parse_observation_table(table, year, month)

        # text = self.parse_observation_table(table)
        # self.dump_to_file(year, month, text)

    def parse_observation_table(self, table, year, month):
        """
        HEADERS = ['Date', 'Temperature (°F)', 'Dew Point (°F)', 'Humidity (%)', 'Wind Speed (mph)', 'Pressure (Hg)', 'Precipitation (in)']
        Parameters
        ----------
        table

        Returns
        -------

        """
        HEADERS = ['date', 't', 'dwpt', 'rh', 'ws', 'pr', 'prcp']
        # # get headers
        # thead = table.find_element_by_tag_name('thead')
        # headers = [td.text for td in thead.find_elements_by_tag_name('td')]
        body = table.find_element_by_tag_name('tbody')
        raw_dfs = pd.read_html(body.get_attribute('innerHTML'))

        for i, df in enumerate(raw_dfs):
            if i == 0:
                df = self.process_date_df(df, year, month, HEADERS[i])
            else:
                # pop first row to col header
                df.columns = f"{HEADERS[i]}_{df.iloc[0]}"
                df = df[1:]

        out = pd.concat(raw_dfs)
        print('debug')

    def process_date_df(self, df, year, month, header):
        """ build the date col """
        df.columns = [header]
        df = df[1:]
        df.loc[header] = df[header].apply(lambda x: datetime(year, month, int(x)).date())
        return df

    def dump_to_file(self, year, month, df):
        dir_ = local.path(__file__).dirname
        new = local.path(dir_ / 'downloads')
        if not new.exists():
            new.mkdir()
        fn = local.path(new / f'{self.station.lower()}_weather_{str(year)}_{str(month)}.csv')
        fn.touch()

        df.to_csv(fn)
        print('data written for date.')


if __name__ == '__main__':
    WeatherScraper().main()
