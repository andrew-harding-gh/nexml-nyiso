import json
import requests


class NoaaClient:
    base_url = "https://api.weather.gov/"
    cp_office = "OKX"
    cp_lat = 40.771133
    cp_long = -73.974187
    gridx, gridy = 33, 37

    def __init__(self):
        pass

    def get_station_info(self, station):
        url = NoaaClient.base_url + f'/stations/{station}'
        data = self.get(url)

    def get_forecast(self, grid=(gridx, gridy)):
        """
        grid: contains x and y coords for station grid; tuple

        Returns
        """
        url = NoaaClient.base_url + f"gridpoints/{NoaaClient.cp_office}/{grid[0]},{grid[1]}"
        return self.get(url)

    def get(self, url):
        r = requests.get(url)
        if r.status_code != 200:
            raise Exception
        return json.loads(r.text)
