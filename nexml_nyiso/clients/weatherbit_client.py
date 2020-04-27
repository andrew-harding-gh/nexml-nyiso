import json
import requests
from datetime import datetime, timedelta

from nexml_nyiso.utility import weather_station, wb_forecast, wb_historical


class WbClient:
    base_url = "https://api.weatherbit.io/v2.0/"
    valid_units = ["I", "M", "S"]  # imperial, metric, scientific

    def __init__(self, api_key):
        self.key = api_key

    # TODO
    def api_key_is_vaild(self):
        pass

    # TODO
    def get_current_key_usage(self):
        """
        https://www.weatherbit.io/api/subscription-usage
        -------
        Returns
        -------

        """
        pass

    def get_historical_by_station_and_day(self, station_id, day, units="I"):
        """
        Fetch weather historical data for one day at a time. This is useful for free tier API key

        Parameters
        ----------
        station_id: str -> string of station ID
        day: str -> %Y-%m-%d format. This is the day (00:00 to 23:59) that we fetch for
        units: str -> measurement system to use for forecast data. Must be in `valid_units`

        Returns list of data points
        -------

        """
        start_date = datetime.strptime(day, "%Y-%m-%d").date()
        end_date = start_date + timedelta(days=1)
        json_ = self.get_historical_weather_by_station(
            station_id=station_id,
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
            units=units
        )

        return json_['data'][0]  # return first and only day as list
        # return wb_historical(**json_['data'][0])

    def get_historical_weather_by_station(self, station_id, start_date, end_date, units="I"):
        """
        https://www.weatherbit.io/api/weather-history-daily
        2,500 historical calls per day on free tier (1 day of data per call)

        Parameters
        ----------
        station_id: str -> string of station ID
        start_date: str -> %Y-%m-%d format. This is the beginning day we fetch the historical for
        end_date: str -> %Y-%m-%d. Data ends before this day
        units: str -> measurement system to use for forecast data. Must be in `valid_units`

        Returns json
        -------

        """
        url = WbClient.base_url + f"/history/daily/?station={station_id}&start_date={start_date}&end_date={end_date}"
        self.check_units(units)
        data = self.get(url, units=units)['data']
        return {
            'station_id': station_id,
            'data': data
        }

    def get_forecast_by_station(self, station_id, days=16, units="I"):
        """
        https://www.weatherbit.io/api/weather-forecast-16-day
        API endpoint returns a 16 day forecast which includes the day the request was made.
        
        station_id: str -> string for station ID to get forecast for
        days_ahead: int -> number of days ahead for forecast to return; eg days=10 => today + 9 days ahead
        units: str -> measurement system to use for forecast data. Must be in `valid_units`

        Returns array containing `wb_forecast` namedtuple for each day in `days`
        """
        url = WbClient.base_url + f"forecast/daily?station={station_id}&days={days}"
        data = self.get(url, units=units)['data']
        return [
                wb_forecast(
                    station_id=station_id,
                    date_fetched=datetime.today().date(),
                    date=datetime.strptime(fc_day.get('valid_date'), "%Y-%m-%d"),
                    # date=fc_day.get('valid_date'),
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

    # TODO: remove units from general method
    def get(self, url, units="I"):
        """
        url: str -> url for request
        units: str -> measurement system to use for forecast data. Must be in `valid_units`

        Returns dict -> dictionary of request response text
        """
        self.check_units(units)
        r = requests.get(url + f"&key={self.key}&units={units}")
        # todo check for no more calls remain
        if r.status_code != 200:
            raise Exception(r.status_code)  # TODO what should do
        return json.loads(r.text)

    @staticmethod
    def check_units(units):
        if units not in WbClient.valid_units:
            raise ValueError(f"Units of type {units} not supported")
