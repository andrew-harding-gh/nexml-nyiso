# Scripts

## Weather Underground Historicals
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