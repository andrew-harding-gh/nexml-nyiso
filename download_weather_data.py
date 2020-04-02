import requests

url = 'http://mis.nyiso.com/public/csv/lfweather/{year}{month:02d}01lfweather_csv.zip'

for year in range(2008, 2021):
    for month in range(1, 13):
        target = url.format(year=year, month=month)
        f = requests.get(target)
        open('data/raw_weather_forecast/' + target.split('/')[-1], 'wb').write(f.content)
        print('Downloaded from: {location}'.format(location=target))
