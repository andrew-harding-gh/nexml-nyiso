# Scripts

## NYISO Electricity Data (Daily and Hourly)
The NYSIO provides almost all of the data used for their own forecasts on their site.

We have produced three scripts for ingesting this data.
- Fetch for electric load
- Process electric load
- Fetch/process weather data

The only nuance to the processing for the electric data is an `HOURLY` boolean in the source code that determines if the output is for hourly/daily data 


## Weather Underground Historicals (Daily Series)
We used WU for our weather historicals as it had a few more data points that were useful beyond what NOAA provided. 

To actual source this data, there is a selenium web crawler that scrapes a monthly table for the NYC LaGuardia Airport weather station.

The script outputs data to a relative folder of `../downloads/`

#### To Run 
##### -- Linux 
- Google Chrome is installed (not Chromium). I downloaded and installed from the chrome `.deb` found here: https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
- `chromedriver` version supports the Chrome version you have installed
##### -- Windows
- Google Chrome is installed
- `chromedriver.exe` is downloaded and supports the Chrome version. (There is no windows driver stored in repo. This will be a manual fetch for the user)
- `CHROMEDRIVER_PATH` in `weather_scraping.py` points to `chromedriver.exe` file

## Weather Underground Historicals (Hourly)
WU was used for our hourly data and was simlply fetched by calling the internal API that 
feeds their site.

This script produces many .csv files that are then aggregated into a large (depending on dates)
.csv for consumption in other programs.

## Weather Underground Historicals (Hourly series)
We have produced a two-phased, two-file script for ingesting this data.
- Fetch (hits WU internal api for hourly data and outputs to files)
- Process (aggregates files and cleans/interpolates missing data before output to new file)
