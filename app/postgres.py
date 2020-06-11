import atexit
import psycopg2
from nexml_nyiso.notebooks.utils import config


class Postgres(object):
    def __init__(self):
        cfg = config['postgres']
        self.conn = psycopg2.connect(
            host=cfg['host'],
            database=cfg['db'],
            user=cfg['user'],
            password=cfg['password']
        )
        atexit.register(self.conn.close)

    def get_hourly_weather(self):
        with self.conn.cursor() as cursor:
            query = '''
                SELECT * FROM hourly_weather;
            '''
            cursor.execute(query)
            return cursor.fetchall()

    def insert_hourly_weather(self, data):
        with self.conn.cursor() as cursor:
            query = '''
            INSERT INTO hourly_weather (
            datetime, 
            location, 
            temp, 
            dwpt, 
            heat_idx, 
            rh, 
            pressure, 
            vis, 
            wc, 
            wdir, 
            wspd, 
            prcp, 
            t_app, 
            uv_idx, 
            clds) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(query, data)
        self.conn.commit()
