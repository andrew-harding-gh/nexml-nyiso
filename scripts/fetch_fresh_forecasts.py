from collections import namedtuple

from plumbum import local

from nexml_nyiso.clients.weatherbit_client import WbClient

wb_station = namedtuple('wb_station', ['full_name', 'id', 'lat', 'long'])
JFK = wb_station('JFK Airport', 'KJFK', 40.65, -73.78)
LGA = wb_station('LaGuardia Airport', 'KLGA', 40.78, -73.88)
KEY = local.env.get('KEY')

client = WbClient(KEY)

print(client.get_hourly_forecast_by_station(LGA.id))
print(client.get_hourly_forecast_by_station(JFK.id))
