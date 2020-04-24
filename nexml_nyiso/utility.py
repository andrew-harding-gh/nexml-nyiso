from collections import namedtuple

""" 
forecast obj:
station id, date of api request, date of forecast, minimum temp, maxmimum temp,  min apparent (real feel) temp,
max apparent (real feel) temp, wind speed, wind direction in degrees, accumulated precipitation, relative humidity
"""
forecast = namedtuple(
    'forecast',
    ['station_id', 'date_fetched', 'date', 'tmin', 'tmax', 'app_tmin', 'app_tmax', 'wspeed', 'wdir', 'prcp', 'rh']
)
weather_station = namedtuple('weather_station', ['station_id', 'name', 'lat', 'lon'])
