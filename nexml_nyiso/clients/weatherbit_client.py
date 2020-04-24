import json
import requests
from datetime import datetime

from plumbum import local

from nexml_nyiso.utility import weather_station, forecast

key = local.env.get('KEY')
central_park = weather_station("USW00094728", "Central Park", 40.7789, -73.9692)


class WbClient:
    base_url = "https://api.weatherbit.io/v2.0/"
    valid_units = ["I", "M", "S"]  # imperial, metric, scientific

    def __init__(self, key):
        self.key = key

    def get_forecast_by_station(self, station_id=central_park.station_id, days=16, units="I"):
        """
        API endpoint returns a 16 day forecast which includes the day the request was made.
        
        station_id: str -> string for station ID to get forecast for
        days_ahead: int -> number of days ahead for forecast to return; eg days=10 => today + 9 days ahead
        units: str -> measurement system to use for forecast data. Must be in `valid_units`

        Returns `forecast` namedtuple
        """
        url = WbClient.base_url + f"forecast/daily?station={station_id}&days={days}"
        self.check_units(units)
        data = self.get(url, units=units)['data']
        return {
            'station_id': station_id,
            'data': [
                forecast(
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
        }

    def get(self, url, units="I"):
        """
        url: str -> url for request
        units: str -> measurement system to use for forecast data. Must be in `valid_units`

        Returns dict -> dictionary of request response text
        """
        self.check_units(units)
        r = requests.get(url + f"&key={self.key}&units={units}")
        if r.status_code != 200:
            raise Exception(r.status_code)  # TODO what should do
        return json.loads(r.text)

    @staticmethod
    def check_units(units):
        if units not in WbClient.valid_units:
            raise ValueError(f"Units of type {units} not supported")
