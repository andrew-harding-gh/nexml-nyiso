import postgres
import pandas as pd


KLGA_HOURLY_PATH = '../data/klga_hourly_weather_historicals.csv'
JFK_HOURLY_PATH = '../data/JFK_hourly_weather_historicals.csv'


# populates hourly_weather table
def populate_weather():
    db = postgres.Postgres()
    jfk = pd.read_csv(JFK_HOURLY_PATH)
    klga = pd.read_csv(KLGA_HOURLY_PATH)
    jfk['location'] = 'jfk'
    klga['location'] = 'klga'
    df = pd.concat([jfk, klga])
    df = df.astype({
        'temp': 'int32',
        'dwpt': 'int32',
        'heat_idx': 'int32',
        'rh': 'int32',
        'pressure': 'int32',
        'vis': 'int32',
        'wc': 'int32',
        'wdir': 'int32',
        'wspd': 'int32',
        'prcp': 'int32',
        't_app': 'int32',
        'uv_idx': 'int32',
    })
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.apply(lambda x: db.insert_hourly_weather((
        x['datetime'],
        x['location'],
        x['temp'],
        x['dwpt'],
        x['heat_idx'],
        x['rh'],
        x['pressure'],
        x['vis'],
        x['wc'],
        x['wdir'],
        x['wspd'],
        x['prcp'],
        x['t_app'],
        x['uv_idx'],
        x['clds'],
    )), axis=1)
    print('Import completed.')


# if __name__ == '__main__':
#     populate_weather()
