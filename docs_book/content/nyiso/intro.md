# Intro

## Objective

To pull energy mix data for NYS from NYISO and check trends for fossil fuel and non-fossil-fuel sources aound the state.


## Data

### Zone shapefiles

From https://www.arcgis.com/home/item.html?id=414d31994ed141f99de84b0d85d1a33a.

To pull from source into a GeoDataFrame:

```python
from climate.nyiso import utils as u
data_folder_path = "./data/"
u.get_zones_archive(data_folder_path=data_folder_path)
u.extract_zones_archive(data_folder_path=data_folder_path)
zones = get_zones(data_folder_path=data_folder_path)
```