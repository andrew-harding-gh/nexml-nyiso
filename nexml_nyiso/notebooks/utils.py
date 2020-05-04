import pandas as pd
import numpy as np
import datetime

START_DATE = datetime.datetime(2005, 2, 1)
END_DATE = datetime.datetime(2020, 3, 30)
WU_WEATHER_PATH = '../../data/klga_weather_historicals.csv'
WEATHER_DATA_PATH = '../../data/noaa_central_park_weather.csv'
PAL_DATA_PATH = '../../data/nyiso_pal_master.csv'
ISOLF_DATA_PATH = '../../data/nyiso_isolf_master.csv'
RANDOM_STATE = 123
DAYS_OF_YEAR = list(range(1, 367))
WEEKDAYS = list(range(7))
WEEKS = list(range(1, 54))
MONTHS = list(range(1, 13))
COLUMNS_TO_NORMALIZE = [
    'target',
    'PRCP',
    'TMAX',
    'TMIN',
]


def date_filter(df):
    return df.loc[(df.index >= START_DATE) & (df.index <= END_DATE)]


def wu_weather():
    df = pd.read_csv(WU_WEATHER_PATH)
    df['date'] = pd.to_datetime(df['date'])
    df['day_of_year'] = df.date.dt.dayofyear
    df['weekday'] = df.date.dt.weekday
    df['week'] = df.date.dt.week
    df['month'] = df.date.dt.month
    df['year'] = df.date.dt.year
    df.set_index('date', inplace=True)
    return date_filter(df)


def noaa_weather():
    df = pd.read_csv(WEATHER_DATA_PATH, dtype='object')
    df['DATE'] = pd.to_datetime(df['DATE'])
    df['day_of_year'] = df.DATE.dt.dayofyear
    df['weekday'] = df.DATE.dt.weekday
    df['week'] = df.DATE.dt.week
    df['month'] = df.DATE.dt.month
    df['year'] = df.DATE.dt.year
    df['TMAX'] = df['TMAX'].astype('float')
    df['TMIN'] = df['TMIN'].astype('float')
    df['PRCP'] = df['PRCP'].astype('float')
    df = df[[
        'day_of_year',
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


def pal():
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


def isolf(forecast_type='isolf_mean'):
    """
    Returns: DataFrame with load forecast. Possible prediction parameters:
    -isolf_min
    -isolf_max
    -isolf_mean (default)
    """
    df = pd.read_csv(ISOLF_DATA_PATH)
    df['Time Stamp'] = pd.to_datetime(df['Time Stamp'])
    df = df[[
        'Time Stamp',
        forecast_type,
    ]]
    df = df.set_index('Time Stamp').sort_index().rename(columns={forecast_type: 'nyiso_prediction'})
    return date_filter(df)


def load_data(target='pal_mean', test_split=0.1):
    """
    Returns: train, test dataframe with specified target column
    """
    unused_targets = list(filter(lambda x: x != target, ['pal_min', 'pal_max', 'pal_mean']))
    weather = noaa_weather()
    actual_load = pal()
    df = actual_load.join(weather, how='inner')
    if df.isnull().values.any():
        print('Null values detected in dataset!')
    df.drop(columns=unused_targets, inplace=True)
    df.rename(columns={target: 'target'}, inplace=True)
    df = df.sample(random_state=RANDOM_STATE, frac=1)
    test, train = np.split(df, [int(test_split * len(df))])
    return train, test


def preprocess(df, mean, std, inplace=True):
    """
    Modifies dataframe in place. Mean and std should be series.

    Parameters
    ----------
    df: DataFrame -> DataFrame to be processed.
    mean: Series -> Series containing mean of columns.
    std: Series -> Series containing std of columns.
    """
    if not inplace:
        df = df.copy(deep=True)

    one_hot(df, 'day_of_year', DAYS_OF_YEAR)
    one_hot(df, 'weekday', WEEKDAYS)
    one_hot(df, 'week', WEEKS)
    one_hot(df, 'month', MONTHS)

    for col in COLUMNS_TO_NORMALIZE:
        if col in list(df.columns):
            df[col] -= mean[col]
            df[col] /= std[col]

    return None if inplace else df


def one_hot(df, column, categories):
    """
    Modifies dataframe in place.
    """
    col_names = [column + '_' + str(x) for x in categories]
    df[col_names] = df[column].apply(lambda x: pd.Series([1 if x == y else 0 for y in categories]))
    df.drop(columns=[column], inplace=True)
