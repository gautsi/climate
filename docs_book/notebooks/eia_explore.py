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
from climate.eia import analysis as a, utils as u
import altair as alt
import pandas as pd
import geopandas as gpd
from pygsutils import data as d

data_path = "./../../data/eia"

# %%
gf = a.GenFuel(loc=data_path)

gf.df.head()

# %% [markdown]
"""
##  US
### Generation over time
"""
# %%
color = alt.Color("general_fuel_type", legend=alt.Legend(title="Fuel type"), sort="descending")

# %% [markdown]
"""
### Generation by fuel
"""

# %%
fm_yr_general = gf.df.groupby(["year", "general_fuel_type"], as_index=False).agg({"gwh": "sum"})


# %%
fm_yr_chrt = (
    alt.Chart(fm_yr_general)
    .mark_bar()
    .encode(
        x="year:O",
        y="gwh",
        color=color,
    )
    .properties(
        title={"text": "US yearly net generation fuel mix", "subtitle": "EIA"}
    )
)

# %%
fm_yr_chrt

# %%
fm_yr_w_ttl = fm_yr_general.merge(
    right=fm_yr_general.groupby(["year"], as_index=False)
    .agg({"gwh": "sum"})
    .rename(columns={"gwh": "ttl_gwh"})
)

# %%
fm_yr_w_ttl["pcnt"] = fm_yr_w_ttl["gwh"] / fm_yr_w_ttl["ttl_gwh"]


# %%
fm_yr_pcnt_chrt = (
    alt.Chart(fm_yr_w_ttl)
    .mark_line()
    .encode(
        x="year:O",
        y=alt.Y("pcnt", axis=alt.Axis(format="%", title="percent")),
        color=color,
    )
    .properties(title={"text": "US yearly generated fuel mix", "subtitle": "EIA"})
)


# %%
fm_yr_pcnt_chrt

# %% [markdown]
"""
##  New York State
### Generation over time
"""

# %% tags=["hide-input"]
ny_month_netgen = (
    gf.df_nys.groupby(["year_month"], as_index=False).agg({"gwh": "sum"})
    # .query("gwh > 0")
)

alt.Chart(ny_month_netgen).mark_bar().encode(x="year_month", y="gwh").configure_axis(
    title=None
).properties(
    title={
        "text": "NYS net generation (GWh) by month",
        "subtitle": "2016-2020, US EIA https://www.eia.gov/electricity/data/eia923/",
    }
)

# %% [markdown]
"""
### Generation by fuel
"""

# %%
fm_yr_general = gf.df_nys.groupby(["year", "general_fuel_type"], as_index=False).agg({"gwh": "sum"})


# %%
fm_yr_chrt = (
    alt.Chart(fm_yr_general)
    .mark_bar()
    .encode(
        x="year:O",
        y="gwh",
        color=color,
    )
    .properties(
        title={"text": "NYS yearly net generation fuel mix", "subtitle": "EIA"}
    )
)

# %%
fm_yr_chrt

# %%
fm_yr_w_ttl = fm_yr_general.merge(
    right=fm_yr_general.groupby(["year"], as_index=False)
    .agg({"gwh": "sum"})
    .rename(columns={"gwh": "ttl_gwh"})
)

# %%
fm_yr_w_ttl["pcnt"] = fm_yr_w_ttl["gwh"] / fm_yr_w_ttl["ttl_gwh"]


# %%
fm_yr_pcnt_chrt = (
    alt.Chart(fm_yr_w_ttl)
    .mark_line()
    .encode(
        x="year:O",
        y=alt.Y("pcnt", axis=alt.Axis(format="%", title="percent")),
        color=color,
    )
    .properties(title={"text": "US yearly generated fuel mix", "subtitle": "EIA"})
)


# %%
fm_yr_pcnt_chrt

# %%
fm_mo = gf.df_nys.groupby(["year_month", "general_fuel_type"], as_index=False).agg({"gwh": "sum"})

# %%
fm_mo_chrt = (
    alt.Chart(fm_mo)
    .mark_bar()
    .encode(
        x="year_month:O",
        y="gwh",
        color=color,
    )
    .properties(
        title={"text": "NYS monthly net generation fuel mix", "subtitle": "EIA"}
    )
)

# %%
fm_mo_chrt

# %%
fm_mo_w_ttl = fm_mo.merge(
    right=fm_mo.groupby(["year_month"], as_index=False)
    .agg({"gwh": "sum"})
    .rename(columns={"gwh": "ttl_gwh"})
)

# %%
fm_mo_w_ttl["pcnt"] = fm_mo_w_ttl["gwh"] / fm_mo_w_ttl["ttl_gwh"]


# %%
fm_mo_pcnt_chrt = (
    alt.Chart(fm_mo_w_ttl)
    .mark_line()
    .encode(
        x="year_month",
        y=alt.Y("pcnt", axis=alt.Axis(format="%", title="percent")),
        color=color,
    )
    .properties(title={"text": "NYS monthly generated fuel mix", "subtitle": "EIA"})
)


# %%
fm_mo_pcnt_chrt

# %% [markdown]
"""
### Dip in nuclear: responsible plants
Which plants had the biggest month-to-month changes in generation between 2020-03-01 and 2020-08-01?
"""

# %%
gf.df_nys[gf.df_nys["year_month"] == "2020-04-01"].head()


# %%
ny_plants = gf.df_nys.groupby(["plant_id", "general_fuel_type", "year_month"], as_index=False).agg(
    {
        "plant_name": u.nonnull_unq_str,
        "operator_name": u.nonnull_unq_str,
        "gwh": "sum",
    }
).query("year_month < '2020-11-01'")

# %%
ny_plants.sort_values("gwh", ascending=False).head()

# %%
ny_plants["prev_gwh"] = ny_plants["gwh"].shift(1)

# %%
ny_plants.sort_values(["plant_id", "year_month"]).head()

# %%
ny_plants["diff"] = ny_plants["gwh"] - ny_plants["prev_gwh"]

# %%
ny_plants.query("year_month >= '2020-01-01'").sort_values("diff").head(10)

# %%
ny_plants.query("year_month >= '2020-01-01'").sort_values("diff", ascending=False).head(10)

# %%
ny_plants_stats = ny_plants.groupby(["plant_id", "plant_name", "operator_name", "general_fuel_type"], as_index=False).agg({"gwh": "sum"}).sort_values("gwh", ascending=False)

# %%
ny_plants_hist = (
    alt.Chart(ny_plants_stats)
    .mark_bar()
    .encode(
        x=alt.X("gwh:Q", bin=True),
        y="count()",
    )
    .properties(title={"text": "NYS total gwh by plant histogram", "subtitle": "EIA"})
)


# %%
ny_plants_hist


# %% [markdown]
"""
### Generation by sector
"""

# %% tags=["hide-input"]
ny_sector_netgen = u.add_sector_desc(
    ny_gf_df.groupby(["eia_sector_number"], as_index=False).agg({"netgen": "sum"})
)
alt.Chart(ny_sector_netgen).mark_bar().encode(
    y=alt.Y("eia_sector_desc", sort="-x"), x="netgen"
).configure_axis(title=None).properties(title="NYS net generation (MWh) by sector")


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

alt.Chart(nyc_month_netgen).mark_bar().encode(
    x="year_month", y="netgen"
).configure_axis(title=None).properties(title="NYC net generation (MWh) by month")

# %% [markdown]
"""
### Generation by sector
"""

# %% tags=["hide-input"]
nyc_sector_netgen = u.add_sector_desc(
    nyc_gf_df.groupby(["eia_sector_number"], as_index=False).agg({"netgen": "sum"})
)
alt.Chart(nyc_sector_netgen).mark_bar().encode(
    y=alt.Y("eia_sector_desc", sort="-x"), x="netgen"
).configure_axis(title=None).properties(title="NYC net generation (MWh) by sector")

# %% [markdown]
"""
##  Queens
### Plant operators
"""

# %%
queens_gf_df = u.add_county(nyc_gf_df, dest_folder=data_path).query(
    "County == 'Queens'"
)
queens_plants = queens_gf_df.groupby(["plant_id"], as_index=False).agg(
    {
        "plant_name": u.nonnull_unq_str,
        "operator_name": u.nonnull_unq_str,
        "netgen": "sum",
    }
)
queens_plants[["operator_name", "plant_name", "netgen"]].sort_values(
    "netgen", ascending=False
).style.format({"netgen": "{:,.0f}"})

# %% [markdown]
"""
### Generation by plant
"""

# %% tags=["hide-input"]
alt.Chart(queens_plants).mark_bar().encode(
    y=alt.Y("plant_name", sort="-x"), x="netgen"
).configure_axis(title=None).properties(title="Queens net generation (MWh) by plant")

# %% [markdown]
"""
###  Map of Queens top plants
"""

# %% tags=["hide-input"]
nbd_gdf = gpd.read_file(
    "https://data.cityofnewyork.us/api/geospatial/cpf4-rkhq?method=export&format=GeoJSON"
)
queens_nbd_gdf = nbd_gdf[nbd_gdf.boro_name == "Queens"]
queens_plants_gdf = u.get_nyc_plants(dest_folder=data_path).query("County == 'Queens'")

queens_top_plants = queens_plants.sort_values("netgen", ascending=False).iloc[:5]
queens_top_plants_gdf = queens_plants_gdf.rename(
    columns={"Plant_Code": "plant_id"}
).merge(
    right=queens_top_plants[["plant_id"]],
    on=["plant_id"],
    how="inner",
    validate="one_to_one",
)

queens_top_nbd_gdf = gpd.sjoin(
    queens_nbd_gdf, queens_top_plants_gdf, how="inner", op="intersects"
)[["ntaname", "geometry"]].drop_duplicates()

queens_top_nbd_gdf.loc[:, "centroid_lat"] = queens_top_nbd_gdf.geometry.centroid.y
queens_top_nbd_gdf.loc[:, "centroid_long"] = queens_top_nbd_gdf.geometry.centroid.x
alt.Chart(queens_top_nbd_gdf).mark_geoshape(
    fill="lightgray", stroke="white"
) + alt.Chart(queens_top_plants_gdf).mark_geoshape() + alt.Chart(
    queens_top_plants_gdf
).mark_text(
    align="left", baseline="middle"
).encode(
    longitude="Longitude",
    latitude="Latitude",
    text="Plant_Name",
) + alt.Chart(
    queens_top_nbd_gdf
).mark_text(
    align="center", baseline="middle"
).encode(
    longitude="centroid_long",
    latitude="centroid_lat",
    text="ntaname",
)

# %%
