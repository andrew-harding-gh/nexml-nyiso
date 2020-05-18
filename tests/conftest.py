import datetime
import pytest

from nexml_nyiso.clients.weatherbit_client import WbClient

RAW_HOURLY_FC = [
    {'wind_cdir': 'NE', 'rh': 79, 'pod': 'd', 'timestamp_utc': '2020-05-18T17:00:00', 'pres': 1020.51,
     'solar_rad': 976.461, 'ozone': 308.795,
     'weather': {'icon': 'c02d', 'code': 801, 'description': 'Few clouds'}, 'wind_gust_spd': 5.9,
     'timestamp_local': '2020-05-18T13:00:00', 'snow_depth': 0, 'clouds': 15, 'ts': 1589821200,
     'wind_spd': 4.55958, 'pop': 0, 'wind_cdir_full': 'northeast', 'slp': 1020.52, 'dni': 924.91,
     'dewpt': 10.5, 'snow': 0, 'uv': 8.87044, 'wind_dir': 38, 'clouds_hi': 15, 'precip': 0, 'vis': 24.1,
     'dhi': 123.25, 'app_temp': 14.2, 'datetime': '2020-05-18:17', 'temp': 14.2, 'ghi': 977.62,
     'clouds_mid': 12, 'clouds_low': 2},
    {'wind_cdir': 'NE', 'rh': 79, 'pod': 'd', 'timestamp_utc': '2020-05-18T18:00:00', 'pres': 1020,
     'solar_rad': 235.075, 'ozone': 310.2,
     'weather': {'icon': 'c04d', 'code': 804, 'description': 'Overcast clouds'}, 'wind_gust_spd': 5.9,
     'timestamp_local': '2020-05-18T14:00:00', 'snow_depth': 0, 'clouds': 100, 'ts': 1589824800,
     'wind_spd': 4.63194, 'pop': 0, 'wind_cdir_full': 'northeast', 'slp': 1020.01, 'dni': 916.71,
     'dewpt': 11, 'snow': 0, 'uv': 2.85233, 'wind_dir': 40, 'clouds_hi': 100, 'precip': 0, 'vis': 24.1,
     'dhi': 121.42, 'app_temp': 14.7, 'datetime': '2020-05-18:18', 'temp': 14.7, 'ghi': 940.3,
     'clouds_mid': 10, 'clouds_low': 1},
    {'wind_cdir': 'NE', 'rh': 80, 'pod': 'd', 'timestamp_utc': '2020-05-18T19:00:00', 'pres': 1019.82,
     'solar_rad': 211.773, 'ozone': 309.03,
     'weather': {'icon': 'c04d', 'code': 804, 'description': 'Overcast clouds'}, 'wind_gust_spd': 6.1,
     'timestamp_local': '2020-05-18T15:00:00', 'snow_depth': 0, 'clouds': 100, 'ts': 1589828400,
     'wind_spd': 4.56151, 'pop': 0, 'wind_cdir_full': 'northeast', 'slp': 1019.82, 'dni': 894.49,
     'dewpt': 11.3, 'snow': 0, 'uv': 2.36962, 'wind_dir': 40, 'clouds_hi': 100, 'precip': 0, 'vis': 24.1,
     'dhi': 116.61, 'app_temp': 14.8, 'datetime': '2020-05-18:19', 'temp': 14.8, 'ghi': 847.09,
     'clouds_mid': 3, 'clouds_low': 3}
]

CLEAN_HOURLY_FC = [
    WbClient.hourly_forecast(station_id='KLGA', dt_fetched=datetime.datetime(2020, 5, 18, 12, 0),
                             datetime=datetime.datetime(2020, 5, 18, 13, 0), temp=14.2, app_temp=14.2, dwpt=10.5, rh=79,
                             wspd=4.55958, wdir=38, wc=7.0, clds='OVC', vis=24.1, pres=1020.51, uv_idx=8.87044, prcp=0,
                             heat_idx=9.0),
    WbClient.hourly_forecast(station_id='KLGA', dt_fetched=datetime.datetime(2020, 5, 18, 12, 0),
                             datetime=datetime.datetime(2020, 5, 18, 14, 0), temp=14.7,
                             app_temp=14.7, dwpt=11, rh=79, wspd=4.63194, wdir=40, wc=7.0,
                             clds='OVC', vis=24.1, pres=1020, uv_idx=2.85233, prcp=0,
                             heat_idx=10.0),
    WbClient.hourly_forecast(station_id='KLGA', dt_fetched=datetime.datetime(2020, 5, 18, 12, 0),
                             datetime=datetime.datetime(2020, 5, 18, 15, 0), temp=14.8, app_temp=14.8, dwpt=11.3, rh=80,
                             wspd=4.56151, wdir=40, wc=7.0, clds='OVC', vis=24.1, pres=1019.82, uv_idx=2.36962, prcp=0,
                             heat_idx=10.0)
    ]