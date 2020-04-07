import os
import requests
import time

from datetime import date
from dateutil.relativedelta import relativedelta
from plumbum import local

start_date = date(2005, 2, 1)  # this is the initial month when NYC is its own region
end_date = date(2020, 3, 1)

base = "http://mis.nyiso.com/public/csv"
date_fmt = "%Y%m%d"

temp_zip = local.path(os.path.dirname(__file__)).up() / 'raw_data' / 'temp.zip'


def process_data_file(data_type, date_obj):
    iso_filename = f"{date_obj.strftime(date_fmt)}{data_type}_csv.zip"
    r = requests.get(
        f"{base}/{data_type}/{iso_filename}",
        stream=True
    )

    if not temp_zip.exists():
        temp_zip.touch()

    with open(temp_zip, 'wb') as file:
        for chunk in r.iter_content(chunk_size=512):
            if chunk:
                file.write(chunk)

    wp = temp_zip.dirname / f"{data_type}_archive"
    if not wp.exists():
        wp.mkdir()

    else:
        temp_zip.move(wp / iso_filename)

    time.sleep(1)  # avoid req flooding


def main():
    cur_date = start_date
    while cur_date <= end_date:
        process_data_file("pal", cur_date)
        process_data_file("isolf", cur_date)
        print(f"Download complete for {cur_date.strftime('%Y-%m-%d')}")
        cur_date += relativedelta(months=+1)


if __name__ == '__main__':
    main()
