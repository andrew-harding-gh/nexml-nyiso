import json
import requests
from collections import namedtuple
from datetime import datetime, timedelta

from nexml_nyiso import utility


class WbClient:
    base_url = "https://api.weatherbit.io/v2.0/"
    valid_units = ["I", "M", "S"]  # imperial, metric, scientific

    hourly_forecast = namedtuple(
        'hourly_forecast',
        [
            'station_id', 'dt_fetched', 'datetime', 'temp', 'app_temp', 'dwpt', 'rh',
            'wspd', 'wdir', 'wc', 'clds', 'vis', 'pres', 'uv_idx', 'prcp', 'heat_idx'
        ]
    )

    daily_forecast = namedtuple(
        'daily_forecast',
        ['station_id', 'date_fetched', 'date', 'tmin', 'tmax', 'app_tmin', 'app_tmax', 'wspeed', 'wdir', 'prcp', 'rh']
    )

    def __init__(self, api_key, units="I"):
        self.key = api_key
        self.units = self.check_units(units)

    # TODO
    def check_api_key(self):
        """ just try to get usage info with KEY; fails fast if KEY is bad """
        pass

    def get_current_key_usage(self):
        url = WbClient.base_url + 'subscriptions/usage'
        return self.get(url)

    def get_historical_by_station_and_day(self, station_id, day):
        """
        Fetch weather historical data for one day at a time. This is useful for free tier API key

        Parameters
        ----------
        station_id: str -> string of station ID
        day: str -> %Y-%m-%d format. This is the day (00:00 to 23:59) that we fetch for
        units: str -> measurement system to use for forecast data. Must be in class attr `valid_units`

        Returns list of data points
        -------

        """
        start_date = datetime.strptime(day, "%Y-%m-%d").date()
        end_date = start_date + timedelta(days=1)
        json_ = self.get_historical_weather_by_station(
            station_id=station_id,
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
        )

        return json_['data'][0]  # return first and only day as list

    def get_historical_weather_by_station(self, station_id, start_date, end_date):
        """
        https://www.weatherbit.io/api/weather-history-daily
        2,500 historical calls per day on free tier (1 day of data per call)

        Parameters
        ----------
        station_id: str -> string of station ID
        start_date: str -> %Y-%m-%d format. This is the beginning day we fetch the historical for
        end_date: str -> %Y-%m-%d. Data ends before this day
        units: str -> measurement system to use for forecast data. Must be in class attr `valid_units`

        Returns json
        -------
        """
        endpoint = "/history/daily/"
        url = WbClient.base_url + endpoint
        params = {
            'station': station_id,
            'start_date': start_date,
            'end_date': end_date
        }
        data = self.get(url, params)['data']
        return data

    def get_hourly_forecast_by_station(self, station_id, hours=48):
        """
        https://www.weatherbit.io/api/weather-forecast-120-hour
        API endpoint returning hourly forecasts beginning with the hour following the current one.

        Parameters
        ----------
        station_id: str -> station ID for weatherbit
        hours: int (1 to 120) -> count of hours ahead to fetch forecast; max on free tier is 48

        Returns
        -------
        """
        endpoint = 'forecast/hourly'
        url = WbClient.base_url + endpoint
        params = {
            'station': station_id,
            'hours': hours
        }
        data = self.get(url, params)['data']
        return {
            'station': station_id,
            'data': [
                WbClient.hourly_forecast(
                    station_id=station_id,
                    # we only care about getting the dt within the hour it was fetched
                    dt_fetched=datetime.fromisoformat(datetime.today().strftime("%Y-%m-%d %H:00:00")),
                    datetime=datetime.fromisoformat(hr_record['timestamp_local']),
                    temp=hr_record['temp'],
                    app_temp=hr_record['app_temp'],
                    dwpt=hr_record['dewpt'],
                    rh=hr_record['rh'],
                    wspd=hr_record['wind_spd'],
                    wdir=hr_record['wind_dir'],
                    clds=utility.convert_cld_cover((hr_record['clouds'])),
                    vis=hr_record['vis'],
                    pres=hr_record['pres'],
                    uv_idx=hr_record['uv'],
                    prcp=hr_record['precip'],
                    heat_idx=utility.calc_heat_index(hr_record['temp'], hr_record['rh']),
                    wc=utility.calc_wind_chill(hr_record['temp'], hr_record['wind_spd'])
                )
                for hr_record in data
            ]
        }

    def get_days_ahead_forecast_by_station(self, station_id, days=16):
        """
        https://www.weatherbit.io/api/weather-forecast-16-day
        API endpoint returns a 16 day forecast which includes the day the request was made.

        Parameters
        ----------
        station_id: str -> string for station ID to get forecast for
        days: int -> number of days ahead for forecast to return; eg days=10 => today + 9 days ahead

        Returns array containing `wb_forecast` namedtuple for each day in `days`
        ----------
        """
        endpoint = "forecast/daily"
        url = WbClient.base_url + endpoint
        params = {
            'station': station_id,
            'days': days
        }
        data = self.get(url, params)['data']
        return [
            WbClient.daily_forecast(
                station_id=station_id,
                date_fetched=datetime.today().date(),
                date=datetime.strptime(fc_day.get('valid_date'), "%Y-%m-%d"),
                tmin=fc_day.get("min_temp"),
                tmax=fc_day.get("max_temp"),
                app_tmin=fc_day.get("app_min_temp"),
                app_tmax=fc_day.get("app_max_temp"),
                wspeed=fc_day.get("wind_spd"),
                wdir=fc_day.get("wind_dir"),
                prcp=fc_day.get("precip"),
                rh=fc_day.get("rh")
            )
            for fc_day in data
        ]

    def get(self, url, query_params=None):
        key_param = {'key': self.key}
        if query_params is None:
            query_params = key_param
        else:
            query_params.update(key_param)
        query_string = "?" + "&".join(f"{k}={v}" for k, v in query_params.items())

        try:
            r = requests.get(url + query_string)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise e
        return json.loads(r.text)

    @staticmethod
    def check_units(units):
        if units not in WbClient.valid_units:
            raise ValueError(f"Units of type {units} not supported. Must be in {str(WbClient.valid_units)}")
        return units
