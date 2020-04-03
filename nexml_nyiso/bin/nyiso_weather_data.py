import requests
import glob
from zipfile import ZipFile
import pandas as pd

url = 'http://mis.nyiso.com/public/csv/lfweather/{year}{month:02d}01lfweather_csv.zip'


def download_files():
    for year in range(2008, 2021):
        for month in range(1, 13):
            target = url.format(year=year, month=month)
            f = requests.get(target)
            if f.status_code == 200:
                open('../raw_data/nyiso_weather_forecast/' + target.split('/')[-1], 'wb').write(f.content)
                print('Downloaded from: {location}'.format(location=target))


def create_csv():
    forecast_data = []
    file_names = glob.glob('../raw_data/nyiso_weather_forecast/*.zip')
    for file in file_names:
        with ZipFile(file) as myzip:
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
    # download_files()
    create_csv()
