from datetime import datetime, timedelta

import pandas as pd
from plumbum import local, cli

from nexml_nyiso.clients import weatherbit_client
from nexml_nyiso.utility import central_park


class WbHistoricals(cli.Application):
    # TODO
    # verbose = cli.Flag(['v', 'verbose'], help='Flag to toggle display of detailed script progress')

    arg_help_str = '{} must be provided. Export `{}` to your environment OR use a flag with value eg.`python -m script --flag=VALUE`'

    units = cli.SwitchAttr(["--units"], str, default='I',
                           help='Retrieve data in unit system: `I`mperial, `S`cientific, or `M`etric')
    api_key = cli.SwitchAttr(['-k', '--api-key'], str, envname="KEY", mandatory=True,
                             help=arg_help_str.format('API Key', 'KEY'))

    @cli.switch(['-s', '--start-date'], str, envname="START_DATE", mandatory=True,
              help=arg_help_str.format('Start Date', 'START_DATE'))
    def set_start_date(self, val):
        self.start_date = datetime.strptime(val, "%Y-%m-%d").date()

    @cli.switch(['-e', '--end-date'], str, envname="END_DATE", mandatory=True, help=arg_help_str.format('End Date', 'END_DATE'))
    def set_end_date(self, val):
        self.end_date = datetime.strptime(val, "%Y-%m-%d").date()

    def main(self):
        cur_date = self.start_date
        client = weatherbit_client.WbClient(api_key=self.api_key)

        data = list()

        while cur_date <= self.end_date:
            try:
                history = client.get_historical_by_station_and_day(
                    station_id=central_park.station_id,
                    day=cur_date,
                    units=self.units
                )
            except Exception as e:
                print(f'Fetch failed on {cur_date} with exception {e}')
                break
            data.append(history)
            cur_date += timedelta(days=1)

        df = pd.DataFrame(data)


if __name__ == '__main__':
    WbHistoricals.run()
