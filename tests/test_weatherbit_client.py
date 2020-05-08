import json
import pytest
from requests.exceptions import HTTPError
from unittest.mock import MagicMock


import requests_mock

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
        'id': 'jfk',
        'year': 2020
    }

    test_url = url + f"?key={TEST_KEY}&id=jfk&year=2020"

    # set a mock landing
    kwargs['mock'].get(test_url, text=json.dumps(BASIC_RESP))
    # ensure we land correctly
    assert client.get(url, query_params) == BASIC_RESP

    # set bad mock landing by overwriting the good landing
    kwargs['mock'].get(test_url, text=json.dumps(BASIC_RESP), status_code=404)
    # ensure we fail to land fast
    with pytest.raises(HTTPError):
        client.get(url, query_params)
