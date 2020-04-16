import pandas as pd
import datetime

START_DATE = datetime.datetime(2005, 2, 1)
END_DATE = datetime.datetime(2020, 3, 30)
WEATHER_DATA_PATH = '../data/central_park_weather.csv'
PAL_DATA_PATH = '../data/nyiso_pal_master.csv'


def date_filter(df):
    return df.loc[(df.index >= START_DATE) & (df.index <= END_DATE)]


def load_weather_data():
    df = pd.read_csv(WEATHER_DATA_PATH, dtype='object')
    df['DATE'] = pd.to_datetime(df['DATE'])
    df['weekday'] = df.DATE.dt.weekday
    df['week'] = df.DATE.dt.week
    df['month'] = df.DATE.dt.month
    df['year'] = df.DATE.dt.year
    df['TMAX'] = df['TMAX'].astype('float')
    df['TMIN'] = df['TMIN'].astype('float')
    df['PRCP'] = df['PRCP'].astype('float')
    df = df[[
        'weekday', 
        'week', 
        'month', 
        'PRCP',
        'TMAX',
        'TMIN',
        'DATE',
    ]]
    df = df.set_index('DATE').sort_index()
    return date_filter(df)


def load_pal_data():
    df = pd.read_csv(PAL_DATA_PATH)
    df['Time Stamp'] = pd.to_datetime(df['Time Stamp'])
    df = df[[
        'Time Stamp',
        'pal_min',
        'pal_max',
        'pal_mean',
    ]]
    df = df.set_index('Time Stamp').sort_index()
    return date_filter(df)
