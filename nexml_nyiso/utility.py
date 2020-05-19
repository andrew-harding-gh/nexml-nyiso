import math
from collections import namedtuple

from plumbum import local

""" 
forecast obj:
station id, date of api request, date of forecast, minimum temp, maxmimum temp,  min apparent (real feel) temp,
max apparent (real feel) temp, wind speed, wind direction in degrees, accumulated precipitation, relative humidity
"""

weather_station = namedtuple('weather_station', ['station_id', 'name', 'lat', 'lon'])

central_park = weather_station("USW00094728", "Central Park", 40.7789, -73.9692)


def round_decorate(decimals=2):
    def real_decorator(func):
        def func_wrapper(*args, **kwargs):
            return round(func(*args, **kwargs), decimals)

        return func_wrapper

    return real_decorator


@round_decorate(decimals=0)
def calc_heat_index(temp, rh):
    """
    formula from: https://www.wpc.ncep.noaa.gov/html/heatindex_equation.shtml
    ----------
    temp: int -> temperature in degrees F
    rh: int -> relative humidity in percentage points

    Returns float
    -------
    """
    simple = 0.5 * (temp + 61.0 + ((temp - 68.0) * 1.2) + (rh * 0.094))
    if simple < 80:
        return simple

    # otherwise we do some crazy regression computation
    base = -42.379 + 2.04901523 * temp + 10.14333127 * rh - .22475541 * temp * \
           rh - .00683783 * temp * temp - .05481717 * rh * rh + .00122874 * \
           temp * temp * rh + .00085282 * temp * rh * rh - .00000199 * temp * temp * rh * rh

    if rh < 13 and 80 < temp < 112:
        adj = ((13 - rh) / 4) * math.sqrt((17 - abs(temp - 95)) / 17)
        return base - adj

    if rh > 85 and 80 < temp < 87:
        adj = ((rh - 85) / 10) * ((87 - temp) / 5)
        return base + adj

    return base


@round_decorate(decimals=0)
def calc_wind_chill(temp, wspd):
    """
    https://www.weather.gov/media/epz/wxcalc/windChill.pdf

    temp: int -> temp in degrees F
    wspd: float -> wind speed in mph

    Returns float
    """
    if wspd <= 3:
        return temp
    return 35.74 + (0.6125 * temp) - (35.75 * wspd ** 0.16) + (0.4275 * temp * wspd ** 0.16)


def convert_cld_cover(percent):
    """
    use oktas (1/8 sky cover units);
    see: https://www.eoas.ubc.ca/courses/atsc113/flying/met_concepts/01-met_concepts/01c-cloud_coverage/images-01c/cloud_cover_table-v2.png
    """

    if percent < 1 / 8:
        return 'CLR'
    elif percent < 3 / 8:
        return 'FEW'
    elif percent < 5 / 8:
        return 'SCT'
    elif percent < 7 / 8:
        return 'BKN'
    else:
        return "OVC"


def get_url():
    return "postgresql://{user}:{pwd}@{host}/{dbname}".format(
        user=local.env.get("DB_USER", "elec"),
        pwd=local.env.get("DB_PASSWORD", "elec"),
        host=local.env.get("DB_HOST", "localhost"),
        dbname=local.env.get("DB_NAME", "elec_db"),
    )
