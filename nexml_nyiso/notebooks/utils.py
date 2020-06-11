import pandas as pd
import numpy as np
import datetime
import os
import configparser

config = configparser.ConfigParser()
CONFIG_PATH = '~/.nexml-nyiso/config'
config.read(os.path.expanduser(CONFIG_PATH))
START_DATE = datetime.datetime(2005, 2, 1)
END_DATE = datetime.datetime(2020, 3, 30)
WU_WEATHER_PATH = '../../data/klga_weather_historicals.csv'
WU_HOURLY_PATH = '../../data/klga_hourly_weather_historicals.csv'
WU_JFK_HOURLY_PATH = '../../data/JFK_hourly_weather_historicals.csv'
WEATHER_DATA_PATH = '../../data/noaa_central_park_weather.csv'
PAL_DATA_PATH = '../../data/nyiso_pal_master.csv'
PAL_HOURLY_PATH = '../../data/nyiso_pal_hourly_master.csv'
ISOLF_DATA_PATH = '../../data/nyiso_isolf_master.csv'
ISOLF_HOURLY_PATH = '../../data/nyiso_isolf_hourly_master.csv'
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
    't_max',
    't_avg',
    't_min',
    'dwpt_max',
    'dwpt_avg',
    'dwpt_min',
    'rh_max',
    'rh_avg',
    'rh_min',
    'ws_max',
    'ws_avg',
    'ws_min',
    'pr_max',
    'pr_avg',
    'pr_min',
    'prcp_total',
    'temp',  # hourly data below
    'dwpt',
    'heat_idx',
    'rh',
    'pressure',
    'vis',
    'wc',
    'wdir',
    'wspd',
    'prcp',
    't_app',
    'uv_idx',
]


def date_filter(df):
    return df.loc[(df.index >= START_DATE) & (df.index <= END_DATE)]


def wu_weather(hourly=False, interpolate_limit=2, location='klga'):
    """
    Returns hourly/daily WU weather.

    Parameters
    ----------
    hourly: Boolean -> If true, returns hourly data.
    interpolate_limit: Int -> Interpolate weather data. 0 disables interpolation. Default set at 2.
    """
    date_col = 'datetime' if hourly else 'date'

    if location == 'klga':
        path = WU_HOURLY_PATH if hourly else WU_WEATHER_PATH
    elif location == 'jfk':
        path = WU_JFK_HOURLY_PATH

    df = pd.read_csv(path)
    df[date_col] = pd.to_datetime(df[date_col])
    expand_dt_col(df, date_col, hourly=True)
    df.set_index(date_col, inplace=True)
    if hourly:
        # do quick one hot
        df = pd.get_dummies(df, columns=['clds'], prefix=['cloud_cover'])
        if interpolate_limit:
            dates = pd.DataFrame(pd.date_range(START_DATE, END_DATE, freq='H')).rename(columns={0: 'date'}).set_index('date')
            df = dates.join(df, how='left')
            df.interpolate(method='nearest', limit=interpolate_limit, inplace=True)
            df.dropna(inplace=True)  # drop the non-interpolated rows
    return date_filter(df).sort_index()


def noaa_weather():
    df = pd.read_csv(WEATHER_DATA_PATH, dtype='object')
    df['DATE'] = pd.to_datetime(df['DATE'])
    expand_dt_col(df, 'DATE')
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


def pal(hourly=False):
    data_path = PAL_HOURLY_PATH if hourly else PAL_DATA_PATH
    df = pd.read_csv(data_path)
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


def isolf_hourly(lookahead=0):
    """
    Returns: DataFrame with load forecast in hourly format.

    Parameters
    ----------
    lookahead: Int -> Number of days ahead for forecast data. For example, a value of 1 will return all load forecasts
    pertaining to the next calendar day. A value of 0 will return all possible forecasts.
    """
    df = pd.read_csv(ISOLF_HOURLY_PATH)
    df.rename(columns={'forecast': 'nyiso_prediction'}, inplace=True)
        
    df['date_pred_made'] = pd.to_datetime(df['date_pred_made'])
    df['date_pred_for'] = pd.to_datetime(df['date_pred_for'])

    if lookahead:
        df['date_pred_for_rounded'] = df['date_pred_for'].dt.floor("D")
        df = df[(df['date_pred_made'] + pd.Timedelta(days=lookahead) == df['date_pred_for_rounded'])]
        df = df.set_index('date_pred_for').sort_index()
        df = df[['nyiso_prediction']]
    else:
        df.sort_values(by=['date_pred_made', 'date_pred_for'], inplace=True)
        df.reset_index(inplace=True)
    return df


def load_data(target='pal_mean', random=True, test_split=0.1, hourly=False, interpolate_limit=2):
    """
    Returns: train, test dataframe with specified target column

    Parameters
    ----------
    target: String -> Target value to use. Possible values: 'pal_min', 'pal_max', 'pal_mean'.
    random: Boolean -> Randomize all data.
    test_split: Float -> Percentage of data to allocate for test DataFrame. Default is 0.1 (10%).
    hourly: Boolean -> If true, returns hourly data.
    interpolate_limit: Int -> Interpolate weather data. 0 disables interpolation. Default set at 2.
    """
    unused_targets = list(filter(lambda x: x != target, ['pal_min', 'pal_max', 'pal_mean']))
    klga = wu_weather(hourly=hourly, interpolate_limit=interpolate_limit)
    jfk = wu_weather(hourly=hourly, interpolate_limit=interpolate_limit, location='jfk')
    weather = klga.join(jfk, how='inner', rsuffix='_jfk')
    actual_load = pal(hourly=hourly)
    df = actual_load.join(weather, how='inner')  # regardless of daily/hourly, still join on index (date vs datetime)
    if df.isnull().values.any():
        print('Null values detected in dataset!')
    df.drop(columns=unused_targets, inplace=True)
    df.rename(columns={target: 'target'}, inplace=True)
    if random:
        df = df.sample(random_state=RANDOM_STATE, frac=1)
    test, train = np.split(df, [int(test_split * len(df))])
    return train, test


def preprocess(df, mean=0, std=0, inplace=True, normalize=True):
    """
    Modifies dataframe in place. Mean and std should be series.

    Parameters
    ----------
    inplace: Boolean -> Modifies DataFrame in place if true, performs deep copy and returns DataFrame if false.
    df: DataFrame -> DataFrame to be processed.
    mean: Series -> Series containing mean of columns.
    std: Series -> Series containing std of columns.
    normalize: Boolean -> Whether or not to normalize the data.
    """
    if not inplace:
        df = df.copy(deep=True)

    one_hot(df, 'day_of_year', DAYS_OF_YEAR)
    one_hot(df, 'weekday', WEEKDAYS)
    one_hot(df, 'week', WEEKS)
    one_hot(df, 'month', MONTHS)

    # check jfk columns as well
    cols = COLUMNS_TO_NORMALIZE + [x + '_jfk' for x in COLUMNS_TO_NORMALIZE]

    if normalize:
        for col in cols:
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


def expand_dt_col(df, date_col, hourly=False):
    """ mutates df in place """
    df['day_of_year'] = df[date_col].dt.dayofyear
    df['weekday'] = df[date_col].dt.weekday
    df['week'] = df[date_col].dt.week
    df['month'] = df[date_col].dt.month
    if hourly:
        df['hour'] = df[date_col].dt.hour


# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back=1):
    dataX, dataY = [], []
    for i in range(len(dataset)-look_back-1):
        dataX.append(dataset.iloc[i:(i+look_back), 0])
        dataY.append(dataset.iloc[i + look_back, 0])
    return np.array(dataX), np.array(dataY)


def time_series_split(df, look_back=60, target_idx=0):
    x = df[:-look_back, :]
    y = df[look_back:, target_idx]
    return x, y


def reshape_(df, steps=1):
    return np.reshape(
        df,
        (df.shape[0], steps, df.shape[1])
    )
