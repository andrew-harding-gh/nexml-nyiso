# Data


## NYISO

The [New York Independent System Operator (NYISO)][1] is our primary source for training data. 

The unprocessed data pulled directly from their archives live in `/raw_data`. This data is processed by scripts in `/scripts` that 
convert the time-series data to daily, finally storing it in `/data`.

NYISO is a goverment org that maintains the reliable operation of the state's energy grid.
The reason this org is interesting to us is that they do a lot of system load forecasting to ensure optimal distribution. We are attempting to replicate this modeling.

#### Source Datasets
[Load Forecasts (ISOLF)][2]  
[Actual Load Results (PAL)][3]  
[Weather History][4]  


#### Processed datasets:
Load forecast historicals (ISOLF)

| Time Stamp | Name               | PTID              | isolf_min                                                               | isolf_max         | isolf_mean         | 
|------------|--------------------|-------------------|-------------------------------------------------------------------------|-------------|--------------|
| $Y-$m-$d   | Name of ISO region | ID of that region | Minimum electrical load value forecast for this day in Megawatts (MWH) | max.. (MWH) | mean.. (MWH) |

Actual Load historicals (PAL)

| Time Stamp | Name               | PTID              | pal_min                                                                       | pal_max         | pal_mean         | 
|------------|--------------------|-------------------|---------------------------------------------------------------------------------|-------------|--------------|
| $Y-$m-$d   | Name of ISO region | ID of that region | Minimum electrical load value actually recorded for this day in Megawatts (MWH) | max.. (MWH) | mean.. (MWH) |


Weather -- Historical actual and forecasted weather utilized by ISO

| header | h2  | 
|--------|------|
| text   | text |


### NOAA  
  
NYC geographical information can be found [here][5].  
  
You can get a grid location by hitting `https://api.weather.gov/points/{latitude},{longitude}` [[example][6]].  
  
Once found, the forecast data can be pulled with `https://api.weather.gov/gridpoints/TOP/{gridX},{gridY}/forecast`[[example][7]].  
  
[Forecast API Information][8]  
Historic weather data can be downloaded from [here][10]. Choose the GHCN-Daily download option [[details][11]].  
  
### NCEI  
  
[NCEI API Information][9]  
  
###  

### Weather history
NOAA provides daily weather summaries, which have been visualized below.  
Maximum temperature by month:  
![Monthly Temp][monthly_temp]  
Maximum temperature:  
![Max Temp][max_temp]  
Maximum temperature (zoomed in):  
![Max Temp Zoomed][max_temp_zoomed]  
Minimum temperature:  
![Min Temp][min_temp]  
Precipitation:  
![Precipitation][precip]  

  
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
[max_temp]: https://github.com/the-great-shazbot/nexml-nyiso/raw/master/data/charts/max_temp_plot.png
[max_temp_zoomed]: https://github.com/the-great-shazbot/nexml-nyiso/raw/master/data/charts/max_temp_zoomed_plot.png
[min_temp]: https://github.com/the-great-shazbot/nexml-nyiso/raw/master/data/charts/min_temp_plot.png
[precip]: https://github.com/the-great-shazbot/nexml-nyiso/raw/master/data/charts/precip_plot.png
[monthly_temp]: https://github.com/the-great-shazbot/nexml-nyiso/raw/master/data/charts/monthly_temp_plot.png