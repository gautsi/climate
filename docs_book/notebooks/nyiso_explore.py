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

# %%
dfp = "./../../data"

log_fp = "./../../logs/get_nyiso.log"

# %%
g.setup_logging(log_fp)

# %%
fm = u.get_fuel_mix(data_folder_path=dfp, agg="year")

# %%
fm.info()

# %%
fm.head()

# %%
start_year = f"{fm.year.min():.0f}"
end_year = f"{fm.year.max():.0f}"
glue("nyiso_start_year", start_year)
glue("nyiso_end_year", end_year)
subtitle = f"{start_year}-{end_year}, NYISO, http://mis.nyiso.com/public/P-63list.htm"

# %%
yr_fm = (
    alt.Chart(fm)
    .mark_bar()
    .encode(
        x="year:O",
        y="gen_gwh",
        color="fuel",
    )
    .properties(title={"text": "NYS yearly generated fuel mix", "subtitle": subtitle})
)

# %%
glue("yr_fm", yr_fm)

# %%
fm_w_ttl = fm.merge(
    right=fm.groupby(["year"], as_index=False)
    .agg({"gen_gwh": "sum"})
    .rename(columns={"gen_gwh": "ttl_gen_gwh"})
)

# %%
fm_w_ttl["pcnt"] = fm_w_ttl["gen_gwh"]/fm_w_ttl["ttl_gen_gwh"]

# %%
yr_fm_pcnt = (
    alt.Chart(fm_w_ttl)
    .mark_line()
    .encode(
        x="year:O",
        y=alt.Y("pcnt", axis=alt.Axis(format='%', title='percent')),
        color="fuel",
    )
    .properties(title={"text": "NYS yearly generated fuel mix", "subtitle": subtitle})
)

# %%
glue("yr_fm_pcnt", yr_fm_pcnt)


# %%
