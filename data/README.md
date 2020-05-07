# Data


## NYISO

The [New York Independent System Operator (NYISO)][1] is our primary source for training data. 

The unprocessed data pulled directly from their archives live in `/raw_data`. This data is processed by scripts in `/scripts` that 
convert the time-series data to daily, finally storing it in `/data`.

NYISO is a goverment org that maintains the reliable operation of the state's energy grid.
The reason this org is interesting to us is that they do a lot of system load forecasting to ensure optimal distribution. We are attempting to replicate this modeling.

Short description of the NYISO model:  
```
The Load Forecast function uses a combination of advanced neural network and regression type 
forecast models to generate its forecasts. The function uses historical load and weather data 
information (including temperature, dew point, cloud cover and wind speed) for each Zone to 
develop Zone load forecast models.
``` 
[[source][16]]

#### Source Datasets:
[Load Forecasts (ISOLF)][2]  
[Actual Load Results (PAL)][3]  
[Weather History][4]  


#### Processed datasets:
Load forecast daily historicals (ISOLF)

| Time Stamp | Name               | PTID              | isolf_min                                                               | isolf_max         | isolf_mean         | 
|------------|--------------------|-------------------|-------------------------------------------------------------------------|-------------|--------------|
| $Y-$m-$d   | Name of ISO region | ID of that region | Minimum electrical load value forecast for this day in Megawatts (MWH) | max.. (MWH) | mean.. (MWH) |

Load forecast (ISOLF) hourly historicals

 | date_pred_for  | date_pred_made       | forecast         | 
|------------|-------------|--------------|
| Datetime the forecast was made for; $Y-$m-$d %h:%m:%s  |   Date the forecast was made on; $Y-$m-$d  |  Electrical load value forecast for this hour in Megawatts (MWH) |


Actual Load daily historicals (PAL)

| Time Stamp | Name               | PTID              | pal_min                                                                       | pal_max         | pal_mean         | 
|------------|--------------------|-------------------|---------------------------------------------------------------------------------|-------------|--------------|
| $Y-$m-$d   | Name of ISO region | ID of that region | Minimum electrical load value actually recorded for this day in Megawatts (MWH) | max.. (MWH) | mean.. (MWH) |

Actual Load (PAL) Hourly historicals

| Time Stamp |  pal_min                                                                        | pal_max     | pal_mean     | 
|------------|---------------------------------------------------------------------------------|-------------|--------------|
| $Y-$m-$d %h:%m:%s   | Minimum electrical load value actually recorded for the hour in Megawatts (MWH) | max.. (MWH) | mean.. (MWH) |




Weather -- Historical actual and forecasted weather utilized by ISO




## NOAA  
  
NYC geographical information can be found [here][5].  
  
You can get a grid location by hitting `https://api.weather.gov/points/{latitude},{longitude}` [[example][6]].  
  
Once found, the forecast data can be pulled with `https://api.weather.gov/gridpoints/TOP/{gridX},{gridY}/forecast` [[example][7]].  
  
[Forecast API Information][8]  
Historic weather data can be downloaded from [here][10]. Choose the GHCN-Daily download option [[details][11]].  

NOAA weather history: 

| DATE     | STATION                                   | LATITUDE          | LONGITUDE         | ELEVATION                                         | PRCP                   | TMAX                     | TMIN                    |TAVG                      |
|----------|-------------------------------------------|-------------------|-------------------|---------------------------------------------------|------------------------|--------------------------|-------------------------|--------------------------|
| $Y-$m-$d | Station ID code (USW00094728 for NYC)     | Decimated degrees | Decimated degrees | Elevation above mean sea level (tenths of meters) | Precipitation (inches) | Highest hourly temp (°F) | Lowest hourly temp (°F) | Average hourly temp (°F) | 
  
Please see the [PDF][13] or the [readme][12] for additional information (there are many more columns in addition to those listed above).
  
### NCEI  
  
[NCEI API Information][9]  

## Weatherbit.io
Free source for a weather forecast API.

16 day forecast endpoint documented [here][14]


## Weather Underground
Source of weather historicals. See an example [here][15]

Dataset has several features, some with with min/max/avg columns: 

| feature           | abbreviation | dtype    | units |
|-------------------|--------------|----------|-------|
| date              | n/a          | datetime | n/a   |
| temperature       | t            | float    | °F    |
| dew point         | dwpt         | float    | °F    |
| relative humidity | rh           | float    | %     |
| wind speed        | ws           | float    | mph   |
| pressure          | pr           | float    | Hg    |
| precipitation     | prcp         | float    | in    |

  
[1]: https://www.nyiso.com/power-grid-data  
[2]: http://mis.nyiso.com/public/P-7list.htm  
[3]: http://mis.nyiso.com/public/P-58Blist.htm
[4]: http://mis.nyiso.com/public/P-7Alist.htm  
[5]: https://tools.wmflabs.org/geohack/geohack.php?pagename=New_York_City&params=40.661_N_73.944_W_region:US-NY_type:city(8175133)  
[6]: https://api.weather.gov/points/40.661,-73.944  
[7]: https://api.weather.gov/gridpoints/TOP/35,32/forecast  
[8]: https://www.weather.gov/documentation/services-web-api  
[9]: https://www.ncei.noaa.gov/support/access-data-service-api-user-documentation  
[10]: https://www.ncdc.noaa.gov/cdo-web/search
[11]: https://www.ncei.noaa.gov/metadata/geoportal/rest/metadata/item/gov.noaa.ncdc:C00861/html
[12]: https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt
[13]: https://www1.ncdc.noaa.gov/pub/data/cdo/documentation/GHCND_documentation.pdf
[14]: https://www.weatherbit.io/api/weather-forecast-16-day
[15]: https://www.wunderground.com/history/monthly/KLGA/date/2005-5
[16]: https://www.nyiso.com/documents/20142/2923301/dayahd-schd-mnl.pdf/0024bc71-4dd9-fa80-a816-f9f3e26ea53a#%5B%7B%22num%22%3A176%2C%22gen%22%3A0%7D%2C%7B%22name%22%3A%22XYZ%22%7D%2C51%2C704%2C0%5D