# Intro

## Plant generation data

See [here](https://www.eia.gov/electricity/data/eia923/) for the data. To pull,

```python
from climate.eia import utils as u
u.pull_data(dest_folder="./../data/eia")
u.get_generation(dest_folder="./../data/eia")
```

This creates a `processed/generation.csv` file with generation data for 2019 and 2020 (through July).


### Original data structure
The generation data appears to be in excel files with many tabs.
|year|filename|most relevant tabs|
|-|-|-|
|2020|EIA923_Schedules_2_3_4_5_M_07_2020_18SEP2020.xlsx|"Page 4 Generator Data", "Page 1 Generation and Fuel Data", "Page 7 File Layout" (data dictionary)|
|2019|EIA923_Schedules_2_3_4_5_M_12_2019_Final.xlsx|"Page 4 Generator Data", "Page 1 Generation and Fuel Data", "Page 7 File Layout" (data dictionary)|
|2018|||
|2017|||