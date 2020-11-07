# Intro

## Plant generation and fuel data

See [here](https://www.eia.gov/electricity/data/eia923/) for the data. To pull,

```python
from climate.eia import utils as u
u.pull_data(dest_folder="./../data/eia")
```

To pull generation and fuel data,

```python
from climate.eia import gen_and_fuel as gf
gf.pull_gen_and_fuel(dest_folder="./../data/eia")
```

This creates a `{dest_folder}/processed/gen_fuel.csv` file with generation and fuel data for 2019 and 2020 (through July) by plant, fuel type, prime mover, year and month.


### Original data structure
The generation and fuel data appears to be in excel files with many tabs.
|year|filename|most relevant tabs|
|-|-|-|
|2020|EIA923_Schedules_2_3_4_5_M_07_2020_18SEP2020.xlsx|"Page 4 Generator Data", "Page 1 Generation and Fuel Data", "Page 7 File Layout" (data dictionary)|
|2019|EIA923_Schedules_2_3_4_5_M_12_2019_Final.xlsx|"Page 4 Generator Data", "Page 1 Generation and Fuel Data", "Page 7 File Layout" (data dictionary)|
|2018|||
|2017|||