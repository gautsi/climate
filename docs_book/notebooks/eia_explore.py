# %% [markdown]
"""
# EIA data: exploring
Exploring EIA data, in particular NYS/NYC/Queens plant generation and fuel mix
"""

# %% tags=["remove-cell"]
from IPython import get_ipython

if get_ipython() is not None:
    get_ipython().run_line_magic("load_ext", "autoreload")
    get_ipython().run_line_magic("autoreload", "2")

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

# %% [markdown]
"""
##  New York State
### Generation over time
"""

# %% tags=["hide-input"]
ny_gf_df = gf_df[gf_df.plant_state == "NY"]

ny_month_netgen = (
    ny_gf_df.groupby(["year_month"], as_index=False)
    .agg({"netgen": "sum"})
    .query("netgen > 0")
)

alt.Chart(ny_month_netgen).mark_bar().encode(x="year_month", y="netgen").configure_axis(
    title=None
).properties(title={
    "text": "NYS net generation (MWh) by month",
    "subtitle": "2019-July 2020, US EIA https://www.eia.gov/electricity/data/eia923/"})

# %% [markdown]
"""
### Generation by sector
"""

# %% tags=["hide-input"]
ny_sector_netgen = u.add_sector_desc(
    ny_gf_df.groupby(["eia_sector_number"], as_index=False)
    .agg({"netgen": "sum"})
)
alt.Chart(ny_sector_netgen).mark_bar().encode(
    y=alt.Y("eia_sector_desc", sort="-x"),
    x="netgen").configure_axis(
    title=None
).properties(title="NYS net generation (MWh) by sector")


# %% [markdown]
"""
## NYC
### Generation over time
"""
# %% tags=["hide-input"]
nyc_gf_df = u.add_nyc_flag(ny_gf_df, dest_folder=data_path).query("nyc == 1")

nyc_month_netgen = (
    nyc_gf_df.groupby(["year_month"], as_index=False)
    .agg({"netgen": "sum"})
    .query("netgen > 0")
)

alt.Chart(nyc_month_netgen).mark_bar().encode(x="year_month", y="netgen").configure_axis(
    title=None
).properties(title="NYC net generation (MWh) by month")

# %% [markdown]
"""
### Generation by sector
"""

# %% tags=["hide-input"]
nyc_sector_netgen = u.add_sector_desc(
    nyc_gf_df.groupby(["eia_sector_number"], as_index=False)
    .agg({"netgen": "sum"})
)
alt.Chart(nyc_sector_netgen).mark_bar().encode(
    y=alt.Y("eia_sector_desc", sort="-x"),
    x="netgen").configure_axis(
    title=None
).properties(title="NYC net generation (MWh) by sector")

# %% [markdown]
"""
##  Queens
### Plant operators
"""

# %%
queens_gf_df =  u.add_county(nyc_gf_df, dest_folder=data_path).query("County == 'Queens'")
queens_plants = queens_gf_df.groupby(["plant_id"], as_index=False).agg(
    {"plant_name": u.nonnull_unq_str,
    "operator_name": u.nonnull_unq_str,
    "netgen": "sum"}
)
queens_plants[["operator_name", "plant_name", "netgen"]].sort_values("netgen", ascending=False).style.format({"netgen": "{:,.0f}"})

# %% [markdown]
"""
### Generation by plant
"""

# %% tags=["hide-input"]
alt.Chart(queens_plants).mark_bar().encode(
    y=alt.Y("plant_name", sort="-x"),
    x="netgen").configure_axis(
    title=None
).properties(title="Queens net generation (MWh) by plant")

# %% [markdown]
"""
###  Map of Queens top plants
"""

# %% tags=["hide-input"]
nbd_gdf = gpd.read_file("https://data.cityofnewyork.us/api/geospatial/cpf4-rkhq?method=export&format=GeoJSON")
queens_nbd_gdf = nbd_gdf[nbd_gdf.boro_name == "Queens"]
queens_plants_gdf = u.get_nyc_plants(dest_folder=data_path).query("County == 'Queens'")

queens_top_plants = queens_plants.sort_values(
    "netgen",
    ascending=False).iloc[:5]
queens_top_plants_gdf = queens_plants_gdf.rename(
    columns={"Plant_Code": "plant_id"}
).merge(
    right=queens_top_plants[["plant_id"]],
    on=["plant_id"],
    how="inner",
    validate="one_to_one"
)

queens_top_nbd_gdf = gpd.sjoin(
    queens_nbd_gdf,
    queens_top_plants_gdf,
    how="inner",
    op="intersects")[["ntaname", "geometry"]].drop_duplicates()

queens_top_nbd_gdf.loc[:,"centroid_lat"] = queens_top_nbd_gdf.geometry.centroid.y
queens_top_nbd_gdf.loc[:,"centroid_long"] = queens_top_nbd_gdf.geometry.centroid.x
alt.Chart(queens_top_nbd_gdf).mark_geoshape(
    fill='lightgray',
    stroke='white'
) + alt.Chart(queens_top_plants_gdf).mark_geoshape(   
) + alt.Chart(queens_top_plants_gdf).mark_text(
    align="left",
    baseline="middle"
).encode(
         longitude="Longitude",
         latitude="Latitude",
         text="Plant_Name",
) + alt.Chart(queens_top_nbd_gdf).mark_text(
    align="center",
    baseline="middle"
).encode(
         longitude='centroid_long',
         latitude='centroid_lat',
         text='ntaname',
     )

# %%
