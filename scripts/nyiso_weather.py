import requests
import glob
import pandas as pd
import datetime
from zipfile import ZipFile
from io import BytesIO

URL = 'http://mis.nyiso.com/public/csv/lfweather/{year}{month:02d}01lfweather_csv.zip'


def create_csv():
    forecast_data = []
    for year in range(2008, datetime.datetime.now().year + 1):
        print('\rDownloading year {year}...'.format(year=year), end='')
        for month in range(1, 13):
            target = URL.format(year=year, month=month)
            f = requests.get(target)
            if f.status_code == 200:
                with ZipFile(BytesIO(f.content)) as myzip:
                    for csv_file in myzip.filelist:
                        with myzip.open(csv_file.filename) as csv:
                            df = pd.read_csv(csv)
                            # Some of the CSVs have a 10th column filled with NaN
                            df = df[[
                                'Forecast Date',
                                'Vintage Date',
                                'Vintage',
                                'Station ID',
                                'Max Temp',
                                'Min Temp',
                                'Max Wet Bulb',
                                'Min Wet Bulb']]
                            df['source_file_name'] = csv_file.filename
                            forecast_data.append(df)
    pd.concat(forecast_data).to_csv('../data/nyiso_weather_forecast.csv', index=False)


if __name__ == "__main__":
    create_csv()
