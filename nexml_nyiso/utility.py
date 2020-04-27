from collections import namedtuple

""" 
forecast obj:
station id, date of api request, date of forecast, minimum temp, maxmimum temp,  min apparent (real feel) temp,
max apparent (real feel) temp, wind speed, wind direction in degrees, accumulated precipitation, relative humidity
"""
wb_forecast = namedtuple(
    'wb_forecast',
    ['station_id', 'date_fetched', 'date', 'tmin', 'tmax', 'app_tmin', 'app_tmax', 'wspeed', 'wdir', 'prcp', 'rh']
)

# interface for weatherbit client historical return for one day
wb_historical = namedtuple(
    'wb_historical',
    ['rh', 'max_wind_spd_ts', 't_ghi', 'max_wind_spd', 'solar_rad', 'wind_gust_spd', 'max_temp_ts', 'min_temp_ts',
     'clouds', 'max_dni', 'precip_gpm', 'wind_spd', 'slp', 'ts', 'max_ghi', 'temp', 'pres', 'dni', 'dewpt', 'snow',
     'dhi', 'precip', 'wind_dir', 'max_dhi', 'ghi', 'max_temp', 't_dni', 'max_uv', 't_dhi', 'datetime', 't_solar_rad',
     'min_temp', 'max_wind_dir', 'snow_depth']
)

weather_station = namedtuple('weather_station', ['station_id', 'name', 'lat', 'lon'])

central_park = weather_station("USW00094728", "Central Park", 40.7789, -73.9692)
