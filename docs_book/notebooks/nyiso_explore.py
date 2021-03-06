# %% [markdown]
"""
# NYISO data: exploring
Exploring NYISO data, in particular electric generation fuel mix over time
"""

# %% tags=['hide-cell']
from IPython import get_ipython

if get_ipython() is not None:
    get_ipython().run_line_magic("load_ext", "autoreload")
    get_ipython().run_line_magic("autoreload", "2")

# %%
from climate.nyiso import utils as u
import logging
from pygsutils import general as g
import pandas as pd
from myst_nb import glue
import altair as alt
import datetime as dt

# %%
dfp = "./../../data"

log_fp = "./../../logs/get_nyiso.log"

# %%
g.setup_logging(log_fp)

# %%
fm = u.get_fuel_mix(data_folder_path=dfp)

# %%
fm.head()

# %%
fm_yr = u.get_fuel_mix(data_folder_path=dfp, agg="year")

# %%
fm_yr.info()

# %%
fm_yr.head()

# %%
start_year = f"{fm_yr.year.min():.0f}"
end_year = f"{fm_yr.year.max():.0f}"
glue("nyiso_start_year", start_year)
glue("nyiso_end_year", end_year)
subtitle = f"{start_year}-{end_year}, NYISO, http://mis.nyiso.com/public/P-63list.htm"

# %%
fm_yr_general = fm_yr.groupby(["year", "general"], as_index=False).agg(
    {"gen_gw": "sum"}
)

# %%
color = alt.Color("general", legend=alt.Legend(title="Fuel type"), sort="descending")

# %%
fm_yr_chrt = (
    alt.Chart(fm_yr_general)
    .mark_bar()
    .encode(
        x="year:O",
        y="gen_gw",
        color=color,
    )
    .properties(title={"text": "NYS yearly generated average fuel mix", "subtitle": subtitle})
)

# %%
glue("fm_yr_chrt", fm_yr_chrt)

# %%
fm_yr_w_ttl = fm_yr_general.merge(
    right=fm_yr_general.groupby(["year"], as_index=False)
    .agg({"gen_gw": "sum"})
    .rename(columns={"gen_gw": "ttl_gen_gw"})
)

# %%
fm_yr_w_ttl["pcnt"] = fm_yr_w_ttl["gen_gw"] / fm_yr_w_ttl["ttl_gen_gw"]

# %%
fm_yr_pcnt_chrt = (
    alt.Chart(fm_yr_w_ttl)
    .mark_line()
    .encode(
        x="year:O",
        y=alt.Y("pcnt", axis=alt.Axis(format="%", title="percent")),
        color=color,
    )
    .properties(title={"text": "NYS yearly generated average fuel mix", "subtitle": subtitle})
)

# %%
glue("fm_yr_pcnt_chrt", fm_yr_pcnt_chrt)


# %%
fm_mo = u.get_fuel_mix(data_folder_path=dfp, agg="month")

# %%
fm_mo_general = fm_mo.groupby(["year", "month", "general"], as_index=False).agg(
    {"gen_gw": "sum"}
)

# %%
def to_dt(row):
    return dt.date(year=row.year, month=row.month, day=1)


fm_mo_general["month_dt"] = pd.to_datetime(fm_mo_general.apply(to_dt, axis=1))

# %%
fm_mo_chrt = (
    alt.Chart(fm_mo_general)
    .mark_bar()
    .encode(
        x="yearmonth(month_dt)",
        y="gen_gw",
        color=color,
    )
    .properties(title={"text": "NYS monthly generated average fuel mix", "subtitle": subtitle})
)

# %%
glue("fm_mo_chrt", fm_mo_chrt)

# %%
fm_mo_line_chrt = (
    alt.Chart(fm_mo_general)
    .mark_line()
    .encode(
        x="yearmonth(month_dt)",
        y="gen_gw",
        color=color,
    )
    .properties(title={"text": "NYS monthly generated average fuel mix", "subtitle": subtitle})
)

# %%
glue("fm_mo_line_chrt", fm_mo_line_chrt)

# %%
fm_mo_w_ttl = fm_mo_general.merge(
    right=fm_mo_general.groupby(["month_dt"], as_index=False)
    .agg({"gen_gw": "sum"})
    .rename(columns={"gen_gw": "ttl_gen_gw"})
)

# %%
fm_mo_w_ttl["pcnt"] = fm_mo_w_ttl["gen_gw"] / fm_mo_w_ttl["ttl_gen_gw"]

# %%
fm_mo_pcnt_chrt = (
    alt.Chart(fm_mo_w_ttl)
    .mark_line()
    .encode(
        x="yearmonth(month_dt)",
        y=alt.Y("pcnt", axis=alt.Axis(format="%", title="percent")),
        color=color,
    )
    .properties(title={"text": "NYS yearly generated average fuel mix", "subtitle": subtitle})
)

# %%
glue("fm_mo_pcnt_chrt", fm_mo_pcnt_chrt)

# %%
fm_mo_pcnt_mo_chrt = (
    alt.Chart(fm_mo_w_ttl)
    .mark_line()
    .encode(
        x="year(month_dt)",
        y=alt.Y("pcnt", axis=alt.Axis(format="%", title=""), scale=alt.Scale(zero=False)),
        color=color,
        row = "month(month_dt):N",
    )
    .properties(title={"text": "NYS yearly generated average fuel mix", "subtitle": subtitle}, height=50, width=100)
)
# %%
fm_mo_pcnt_mo_chrt

# %%
fm_mo_w_avg = fm_mo_general.merge(
    right = fm_mo_general.groupby(["general", "month"], as_index=False).agg({"gen_gw": "mean"}).rename(columns={"gen_gw": "avg_gen_gw"}),
    on=["general", "month"],
    how="left",
    validate="many_to_one")

# %%
fm_mo_w_avg["gen_gw_diff"] = fm_mo_w_avg.gen_gw - fm_mo_w_avg.avg_gen_gw

# %%
fm_mo_diff_chrt = (
    alt.Chart(fm_mo_w_avg)
    .mark_line()
    .encode(
        x="yearmonth(month_dt)",
        y="gen_gw_diff",
        color=color,
    )
    .properties(title={"text": "NYS monthly generated average fuel mix: difference from month average", "subtitle": subtitle})
)
# %%
fm_mo_diff_chrt

# %%
fm_mo_w_avg_pcnt = fm_mo_w_ttl.merge(
    right = fm_mo_w_ttl.groupby(["general", "month"], as_index=False).agg({"pcnt": "mean"}).rename(columns={"pcnt": "avg_pcnt"}),
    on=["general", "month"],
    how="left",
    validate="many_to_one")
# %%
fm_mo_w_avg_pcnt

# %%
fm_mo_w_avg_pcnt["pcnt_diff"] = fm_mo_w_avg_pcnt.pcnt - fm_mo_w_avg_pcnt.avg_pcnt

# %%
fm_mo_pcnt_diff_chrt = (
    alt.Chart(fm_mo_w_avg_pcnt)
    .mark_line()
    .encode(
        x="yearmonth(month_dt)",
        y=alt.Y("pcnt_diff", axis=alt.Axis(format="%", title="percent difference"), scale=alt.Scale(zero=False)),
        color=color,
    )
    .properties(title={"text": "NYS monthly generated average fuel mix: percent difference from month average", "subtitle": subtitle})
)
# %%
fm_mo_pcnt_diff_chrt

# %%
fm_mo_rolling_chrt = (
    alt.Chart(fm_mo_general)
    .transform_window(
        sort=[{"field":"month_dt"}],
        groupby=["general"],
        frame=[-12,0],
        rolling_gen_gw = "mean(gen_gw)")
    .mark_line()
    .encode(
        x="yearmonth(month_dt)",
        y=alt.Y("rolling_gen_gw:Q", scale=alt.Scale(zero=False)),
        color=color,
    )
    .properties(title={"text": "NYS monthly generated average fuel mix: rolling 12-month average", "subtitle": subtitle})
)
# %%
glue("fm_mo_rolling_chrt", fm_mo_rolling_chrt)


# %%
fm_mo_rolling_pcnt_chrt = (
    alt.Chart(fm_mo_w_ttl)
    .transform_window(
        sort=[{"field":"month_dt"}],
        groupby=["general"],
        frame=[-12,0],
        rolling_pcnt = "mean(pcnt)")
    .mark_line()
    .encode(
        x="yearmonth(month_dt)",
        y=alt.Y("rolling_pcnt:Q", axis=alt.Axis(format="%"), scale=alt.Scale(zero=False)),
        color=color,
    )
    .properties(title={"text": "NYS monthly generated average fuel mix: rolling 12-month average percent", "subtitle": subtitle})
)
# %%
glue("fm_mo_rolling_pcnt_chrt", fm_mo_rolling_pcnt_chrt)

# %%
fm_mo_pcnt_yr_chrt = (
    alt.Chart(fm_mo_w_ttl)
    .mark_line()
    .encode(
        x="month(month_dt)",
        y=alt.Y("pcnt", axis=alt.Axis(format="%", title="percent")),
        row="general",
        color="year(month_dt):O",
    )
    .properties(title={"text": "NYS yearly generated average fuel mix", "subtitle": subtitle}, height=100)
)
# %%
fm_mo_pcnt_yr_chrt
# %%
