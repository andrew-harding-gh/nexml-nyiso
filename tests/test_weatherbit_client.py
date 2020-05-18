import json
import pytest
from datetime import datetime
from requests.exceptions import HTTPError
from unittest.mock import MagicMock

import requests_mock
from freezegun import freeze_time

from tests import conftest
from nexml_nyiso.clients.weatherbit_client import WbClient

"""
Goofy **kwargs syntax for mocking requests can be explained by pytest searching for fixtures clashing with the
requests_mock functionality. See, https://requests-mock.readthedocs.io/en/latest/mocker.html#decorator
"""

TEST_KEY = 'abc123'
BASIC_RESP = {'status': 'ok'}


def test_check_units():
    with pytest.raises(ValueError):
        WbClient.check_units('trump_wrong.mp4')

    assert WbClient.check_units("I") == "I"  # pass through works when its valid


@requests_mock.Mocker(kw='mock')
def test_wb_get(**kwargs):
    """ mock the real request, and if the client calls the url we expect, return the processed json """
    client = WbClient(TEST_KEY)

    url = "http://test.com"
    query_params = {
        'station': 'jfk',
        'year': 2020
    }

    test_url = url + f"?key={TEST_KEY}&station=jfk&year=2020"

    # set a mock landing
    kwargs['mock'].get(test_url, text=json.dumps(BASIC_RESP))
    # ensure we land correctly
    assert client.get(url, query_params) == BASIC_RESP

    # set bad mock landing by overwriting the good landing
    kwargs['mock'].get(test_url, text=json.dumps(BASIC_RESP), status_code=404)
    # ensure we fail to land, fast
    with pytest.raises(HTTPError):
        client.get(url, query_params)


@freeze_time("2020-05-18 12:00:00")
@requests_mock.Mocker(kw='mock')
def test_get_hourly_forecast_by_station(**kwargs):
    assert datetime.now() == datetime(2020, 5, 18, 12, 0, 0)

    test_params = {'station': 'KLGA', 'hours': 3}
    # ordering of query params in url depends on order of params passed to function
    expected_url = WbClient.base_url + 'forecast/hourly' +\
                   f"?station={test_params['station']}&hours={test_params['hours']}&key={TEST_KEY}"

    json_return = {
        'some_key': 1,
        'data': conftest.RAW_HOURLY_FC,
        'more_keys': 'here'
    }

    # set a mock response for where we expect to land
    kwargs['mock'].get(expected_url, text=json.dumps(json_return))

    client = WbClient(TEST_KEY)
    result = client.get_hourly_forecast_by_station(test_params['station'], test_params['hours'])

    expected_result = {
        'station': test_params['station'],
        'data': conftest.CLEAN_HOURLY_FC
    }

    assert result == expected_result


