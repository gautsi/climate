# Intro

## Plant generation data

See [here](https://www.eia.gov/electricity/data/eia923/) for the data. To pull,

```python
from climate.eia import utils as u
u.pull_data(dest_folder="./../data/eia")
```
