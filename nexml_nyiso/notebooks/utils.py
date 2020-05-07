import pandas as pd
import numpy as np
import datetime

START_DATE = datetime.datetime(2005, 2, 1)
END_DATE = datetime.datetime(2020, 3, 30)
WU_WEATHER_PATH = '../../data/klga_weather_historicals.csv'
WU_HOURLY_PATH = '../../data/klga_hourly_weather_historicals.csv'
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
]


def date_filter(df):
    return df.loc[(df.index >= START_DATE) & (df.index <= END_DATE)]


def wu_weather():
    df = pd.read_csv(WU_WEATHER_PATH)
    df['date'] = pd.to_datetime(df['date'])
    expand_dt_col(df, 'date')
    df.set_index('date', inplace=True)
    return date_filter(df)


def wu_weather_hourly():
    df = pd.read_csv(WU_HOURLY_PATH)
    df['datetime'] = pd.to_datetime(df['datetime'])
    expand_dt_col(df, 'datetime')
    # also expand hour of day
    df['hour'] = df['datetime'].dt.hour
    df.set_index('datetime', inplace=True)
    # do quick one hot
    df = pd.get_dummies(df, columns=['clds'], prefix=['cloud_cover'])
    return date_filter(df)


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


def pal_hourly():
    df = pd.read_csv(PAL_HOURLY_PATH)
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


def isolf_hourly():
    """
    Returns: DataFrame with load forecast in hourly format.
    ! No index is set
    """
    df = pd.read_csv(ISOLF_HOURLY_PATH)
    df.rename(colummns={'forecast': 'nyiso_prediction'}, inplace=True)
    df.sort_values(by=['date_pred_made', 'date_pred_for'], inplace=True)
    return df


def load_data(target='pal_mean', random=True, test_split=0.1, hourly=False):
    """
    Returns: train, test dataframe with specified target column
    """
    unused_targets = list(filter(lambda x: x != target, ['pal_min', 'pal_max', 'pal_mean']))
    weather = wu_weather_hourly() if hourly else wu_weather()
    actual_load = pal_hourly() if hourly else pal()
    df = actual_load.join(weather, how='inner')  # regardless of daily/hourly, still join on index (date vs datetime)
    if df.isnull().values.any():
        print('Null values detected in dataset!')
    df.drop(columns=unused_targets, inplace=True)
    df.rename(columns={target: 'target'}, inplace=True)
    if random:
        df = df.sample(random_state=RANDOM_STATE, frac=1)
    test, train = np.split(df, [int(test_split * len(df))])
    return train, test


def preprocess(df, mean, std, inplace=True):
    """
    Modifies dataframe in place. Mean and std should be series.

    Parameters
    ----------
    inplace: Boolean -> Modifies DataFrame in place if true, performs deep copy and returns DataFrame if false.
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


def expand_dt_col(df, date_col):
    """ mutates df in place """
    df['day_of_year'] = df[date_col].dt.dayofyear
    df['weekday'] = df[date_col].dt.weekday
    df['week'] = df[date_col].dt.week
    df['month'] = df[date_col].dt.month


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


if __name__ == '__main__':
    load_data(hourly=True)