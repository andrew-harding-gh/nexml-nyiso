# NYISO  

# Data sources: 
### NYISO  
[Main Site][1]  
The forecasting archive is located [here][2].  
The load results are located [here][3].  
The weather data is located [here][4].  

### NOAA  
  
NYC geographical information can be found [here][5].  
  
You can get a grid location by hitting `https://api.weather.gov/points/{latitude},{longitude}` [[example]][6]  
  
Once found, the forecast data can be pulled with `https://api.weather.gov/gridpoints/TOP/{gridX},{gridY}/forecast`[[example]][7]  
  
[Forecast API Information][8]  
Historic weather data can be downloaded from [here][10]  
  
### NCEI  
  
[NCEI API Information][9]  
  
###  
  
[1]: https://www.nyiso.com/power-grid-data  
[2]: http://mis.nyiso.com/public/P-7list.htm  
[3]: http://mis.nyiso.com/public/P-58Clist.htm  
[4]: http://mis.nyiso.com/public/P-7Alist.htm  
[5]: https://tools.wmflabs.org/geohack/geohack.php?pagename=New_York_City&params=40.661_N_73.944_W_region:US-NY_type:city(8175133)  
[6]: https://api.weather.gov/points/40.661,-73.944  
[7]: https://api.weather.gov/gridpoints/TOP/35,32/forecast  
[8]: https://www.weather.gov/documentation/services-web-api  
[9]: https://www.ncei.noaa.gov/support/access-data-service-api-user-documentation  
[10]: https://www.ncdc.noaa.gov/cdo-web/search
