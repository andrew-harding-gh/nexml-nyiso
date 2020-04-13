# Data


## NYISO

NYISO is our primary source for training data. 

The unprocessed data pulled directly from their archives live in `/raw_data`. This data is processed by scripts in `/scripts` that 
convert the time-series data to daily, finally storing it in `/data`.

Three datasets:
- ISOLF -- Historical forecasting done by the ISO

| Time Stamp | Name               | PTID              | isolf_min                                                               | max         | mean         | 
|------------|--------------------|-------------------|-------------------------------------------------------------------------|-------------|--------------|
| $Y-$m-$d   | Name of ISO region | ID of that region | Minimum electrical load value forecast for this day in Megawatts (MWH) | max.. (MWH) | mean.. (MWH) |
- PAL -- Historical actual load data monitored by ISO

| Time Stamp | Name               | PTID              | isolf_min                                                                       | max         | mean         | 
|------------|--------------------|-------------------|---------------------------------------------------------------------------------|-------------|--------------|
| $Y-$m-$d   | Name of ISO region | ID of that region | Minimum electrical load value actually recorded for this day in Megawatts (MWH) | max.. (MWH) | mean.. (MWH) |
- Weather -- Historical actual and forecasted weather utilized by ISO