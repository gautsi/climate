# %% [markdown]
"""
# Fuel mix
Checking fuel mix of NYS/NYC/Queens plants
"""

# %% [markdown]
"""
Previewing generation and fuel data...
"""

# %% tags=["hide-input"]
from climate.eia import utils as u
from climate.eia import gen_and_fuel as gf
import altair as alt
import pandas as pd
import geopandas as gpd

data_path = "./../../data/eia"
gf_df = gf.get_gen_and_fuel(dest_folder=data_path)
gf_df.head()


# %%
