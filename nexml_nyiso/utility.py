import datetime
import pandas as pd

CONSTANTS = {
    'start_date': datetime.datetime(2005, 2, 1),
    'end_date': datetime.datetime(2020, 3, 30),
}


def date_filter(df, date_col, start_date=CONSTANTS['start_date'], end_date=CONSTANTS['end_date']):
    """ expects date column as string and start/end in datetime.datetime/date   """
    return df.loc[(df[date_col] >= start_date) & (df[date_col] <= end_date)]


def load_weather_data():
    df = pd.read_csv('../data/central_park_weather_data.csv', dtype='object')
    df['DATE'] = pd.to_datetime(df['DATE'])
    df = date_filter(df, 'DATE')
    df['weekday'] = df.DATE.dt.weekday
    df['week'] = df.DATE.dt.week
    df['month'] = df.DATE.dt.month
    df['year'] = df.DATE.dt.year
    df['TMAX'] = df['TMAX'].astype('float')
    df['TMIN'] = df['TMIN'].astype('float')
    df['PRCP'] = df['PRCP'].astype('float')
    return df


def load_pal_data():
    df = pd.read_csv('../data/nyiso_pal_master.csv')
    df['Time Stamp'] = pd.to_datetime(df['Time Stamp'])
    df = date_filter(df, 'Time Stamp')
    return df
