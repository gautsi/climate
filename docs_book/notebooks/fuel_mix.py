# %% [markdown]
"""
# Fuel mix

```{note}
The page records my explorations of the fuel mix data from EIA, and will be light on comments and documentation. 
```

Checking fuel mix of largest NYC/Queens plants
"""

# %% tags=["hide-cell"]
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
from myst_nb import glue

data_path = "./../../data/eia"

# %%
gf = a.GenFuel(loc=data_path)

# %%
gf.df.head()

# %%
start_year = gf.df.query("quantity > 0").year.min()
end_year = gf.df.query("quantity > 0").year.max()
glue("start_year", start_year)
glue("end_year", end_year)

subtitle = (
    f"{start_year}-{end_year}, US EIA https://www.eia.gov/electricity/data/eia923/"
)

# %% [markdown]
"""
## Largest NYC plants (by generation)
"""


# %%
gf.df_nyc.head()

# %%
ttl_nyc_gwh = gf.df_nyc.gwh.sum()
glue("ttl_nyc_gwh", "{:,.0f}".format(ttl_nyc_gwh))
glue(
    "avg_nyc_gwh_per_month",
    "{:,.0f}".format(ttl_nyc_gwh / gf.df_nyc.year_month.nunique()),
)

# %%
nyc_year_gwh = (
    gf.df_nyc.assign(year_str=gf.df_nyc.year.astype(str))
    .groupby(["year_str"], as_index=False)
    .agg({"gwh": "sum"})
    .query("gwh > 0")
)

nyc_year_gwh_chart = (
    alt.Chart(nyc_year_gwh)
    .mark_bar()
    .encode(x="year_str", y="gwh")
    .configure_axis(title=None)
    .properties(
        title={
            "text": "NYC net generation (GWh) by year",
            "subtitle": subtitle,
        },
        width=300,
        height=150,
    )
)
glue("nyc_year_gwh_chart", nyc_year_gwh_chart)


# %%
borough_gwh = gf.df_nyc.groupby(["borough"], as_index=False).agg(
    {"gwh": "sum"}
)

# %%
borough_gwh["pcnt"] = borough_gwh.gwh / borough_gwh.gwh.sum()
glue(
    "queens_gwh_pcnt",
    "{:.0%}".format(borough_gwh.query("borough == 'Queens'").iloc[0]["pcnt"]),
)

# %%

borough_gwh_chart = (
    alt.Chart(borough_gwh)
    .mark_bar()
    .encode(x="gwh", y=alt.Y("borough", sort="-x"))
    .configure_axis(title=None)
    .properties(
        title={
            "text": "NYC net generation (GWh) by borough",
            "subtitle": subtitle,
        }
    )
)
glue("borough_gwh_chart", borough_gwh_chart)


# %%
glue("top_ten_pcnt", "{:.0%}".format(gf.df_nyc_plants_top.gwh.sum() / gf.df_nyc_plants.gwh.sum()))
glue("top_ten_queens", len(gf.list_nyc_plants_top_queens))

# %%
nyc_top_plants_table = (
    gf.df_nyc_plants_top.sort_values("gwh", ascending=False)[
        ["operator_name", "plant_name", "borough", "gwh"]
    ]
    .style.format({"gwh": "{:,.0f}"})
    .bar(subset=["gwh"])
    .apply(u.highlight_queens, subset=["borough"])
    .set_table_styles(u.table_styles)
    .hide_index()
    .set_caption(subtitle)
)

glue("nyc_top_plants_table", nyc_top_plants_table)

# %%
nyc_fuel = gf.df_nyc.groupby(
    ["fuel_desc", "physical_unit_label"], as_index=False
).agg({"elec_quantity": "sum", "gwh": "sum"})
nyc_fuel["gwh_pcnt"] = nyc_fuel.gwh / nyc_fuel.gwh.sum()
glue(
    "nat_gas_nyc_pcnt",
    "{:.0%}".format(nyc_fuel.query("fuel_desc == 'Natural Gas'").iloc[0]["gwh_pcnt"]),
)
# %%

nyc_fuel_table = (
    nyc_fuel.sort_values("gwh", ascending=False)
    .style.format({"elec_quantity": "{:,.0f}", "gwh": "{:,.0f}", "gwh_pcnt": "{:.2%}"})
    .set_table_styles(u.table_styles)
    .hide_index()
    .set_caption(subtitle)
)

glue("nyc_fuel_table", nyc_fuel_table)

# %%
gf.df_nyc_plants_top_queens.plant_name.unique()

# %%
glue(
    "nat_gas_queens_pcnt",
    "{:.0%}".format(
        gf.df_top_queens.query("fuel_desc == 'Natural Gas'").elec_quantity.sum()
        / gf.df_nyc.query("fuel_desc == 'Natural Gas'").elec_quantity.sum()
    ),
)

# %%
queens_fuel = gf.df_top_queens.groupby(
    ["fuel_desc", "physical_unit_label"], as_index=False
).agg({"elec_quantity": "sum", "gwh": "sum"})
queens_fuel["gwh_pcnt"] = queens_fuel.gwh / queens_fuel.gwh.sum()
queens_fuel_w_nyc = queens_fuel.merge(
    right=nyc_fuel[["fuel_desc", "elec_quantity"]].rename(
        columns={"elec_quantity": "ttl_nyc_elec_quantity"}
    ),
    on=["fuel_desc"],
    how="left",
    validate="one_to_one",
)
queens_fuel_w_nyc["elec_quantity_pcnt_of_nyc"] = (
    queens_fuel_w_nyc.elec_quantity / queens_fuel_w_nyc.ttl_nyc_elec_quantity
)

queens_fuel_table = (
    queens_fuel_w_nyc.sort_values("gwh", ascending=False)
    .drop(columns=["ttl_nyc_elec_quantity"])
    .style.format(
        {
            "elec_quantity": "{:,.0f}",
            "gwh": "{:,.0f}",
            "gwh_pcnt": "{:.2%}",
            "elec_quantity_pcnt_of_nyc": "{:.2%}",
        }
    )
    .set_table_styles(u.table_styles)
    .hide_index()
    .set_caption("2019-July 2020, US EIA https://www.eia.gov/electricity/data/eia923/")
)

glue("queens_fuel_table", queens_fuel_table)


# %%
# queens plant info


# %%
for i in gf.df_nyc_plants_top_queens.plant_id.values:
    plant_info = gf.df_nyc_plants_top_queens.query(f"plant_id == {i}").iloc[0]
    glue(f"queens_top_gwh_pcnt_{i}", "{:.0%}".format(plant_info.gwh / ttl_nyc_gwh))

    plant_gf_df = gf.df_top_queens.query(f"plant_id == {i}")
    plant_gen_year = (
        plant_gf_df.assign(year_str=plant_gf_df.year.astype(str))
        .groupby(["year_str"], as_index=False)
        .agg({"gwh": "sum"})
        .query("gwh > 0")
    )

    plant_year_gwh_chart = (
        alt.Chart(plant_gen_year)
        .mark_bar()
        .encode(x="year_str", y="gwh")
        .configure_axis(title=None)
        .properties(
            title={
                "text": f"{plant_info['plant_name']} net generation (GWh) by month",
                "subtitle": subtitle,
            },
            width=300,
            height=150,
        )
    )
    glue(f"queens_top_year_gwh_chart_{i}", plant_year_gwh_chart)

    glue(
        f"queens_top_nat_gas_pcnt_{i}",
        "{:.0%}".format(
            plant_gf_df.query("fuel_desc == 'Natural Gas'").elec_quantity.sum()
            / gf.df_nyc.query("fuel_desc == 'Natural Gas'").elec_quantity.sum()
        ),
    )

    plant_fuel = plant_gf_df.groupby(
        ["fuel_desc", "physical_unit_label"], as_index=False
    ).agg({"elec_quantity": "sum", "gwh": "sum"})
    plant_fuel["gwh_pcnt"] = plant_fuel.gwh / plant_fuel.gwh.sum()
    plant_fuel_w_nyc = plant_fuel.merge(
        right=nyc_fuel[["fuel_desc", "elec_quantity"]].rename(
            columns={"elec_quantity": "ttl_nyc_elec_quantity"}
        ),
        on=["fuel_desc"],
        how="left",
        validate="one_to_one",
    )
    plant_fuel_w_nyc["elec_quantity_pcnt_of_nyc"] = (
        plant_fuel_w_nyc.elec_quantity / plant_fuel_w_nyc.ttl_nyc_elec_quantity
    )

    plant_fuel_table = (
        plant_fuel_w_nyc.query("elec_quantity > 0")
        .sort_values("gwh", ascending=False)
        .drop(columns=["ttl_nyc_elec_quantity"])
        .style.format(
            {
                "elec_quantity": "{:,.0f}",
                "gwh": "{:,.0f}",
                "gwh_pcnt": "{:.2%}",
                "elec_quantity_pcnt_of_nyc": "{:.2%}",
            }
        )
        .set_table_styles(u.table_styles)
        .hide_index()
        .set_caption(
            subtitle
        )
    )

    glue(f"queens_top_fuel_table_{i}", plant_fuel_table)

# %%
