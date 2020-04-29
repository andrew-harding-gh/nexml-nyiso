# NYISO  

Nexient ML project aiming to predict daily electrical load of NYC given feature inputs like weather or economic factors.

Currently lives in this personal repo until a more permanent location can be found. 

# Data 

This project uses electrical load and weather historicals and forecasts to be able to do short term forecasting. 

For a more detailed look at each data source, see the [Data README](data/README.md)

# Key terminology  
PAL -> Actual load  
ISOLF -> ISO load forecasts  

# Setup

For now, we recommend setting up a virtual environment to run the scripts and notebooks contained in this project. For more information, please read [here](https://docs.python.org/3/library/venv.html).  
 *  Once created, install `requirements.txt`. 
 *  To train the models you will want to set up [plaidML](https://github.com/plaidml/plaidml) as your backend. If you can run `plaidbench keras mobilenet` without issue the notebooks should run correctly. Alternatively, feel free to modify the notebooks to use anything else compatible with Keras (TensorFlow, Theano, CNTK).  
 
 # Scripts
 
There are several scripts that were used to fetch our datasets. Some of these are packaged and available in `/bin` as bash cmds 

For more detailed documentation, see [Scripts Readme](scripts/README.md)