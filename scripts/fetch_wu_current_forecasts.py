import json
import requests
from collections import namedtuple
from datetime import datetime
from dateutil.relativedelta import relativedelta
from string import Template

import pandas as pd

from nexml_nyiso.notebooks.utils import START_DATE, END_DATE

wu_station = namedtuple('wu_station', ['name', 'wu_name', 'lat', 'long'])
JFK = wu_station('JFK', 'KJFK', 40.65, 73.78)
LGA = wu_station('LGA', 'KLGA', 40.77, 73.86)
KEY = '6532d6454b8aa370768e63d6ba5a832e'






def get_(url):
    r = requests.get(url)

    if r.status_code != 200:
        raise Exception(f'{r.status_code} from request to {url}')

    return json.loads(r.text)


def main(station):
    base_url = Template('https://api.weather.com/v3/wx/forecast/daily/15day?apiKey=$key&geocode=$lat%2C-$long&language=en-US&units=e&format=json')
    url = base_url.substitute(dict(station._asdict()), key=KEY)

    data = get_(url)




if __name__ == '__main__':
    main(JFK)