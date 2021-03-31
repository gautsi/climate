# process eia data

# %% tags=['hide-cell']
from IPython import get_ipython

if get_ipython() is not None:
    get_ipython().run_line_magic("load_ext", "autoreload")
    get_ipython().run_line_magic("autoreload", "2")

# %%
from pygsutils import general as g, cache as c
import logging

# %%
loc = "./../../data/eia"
fp_log = f"{loc}/log_process_eia.log"

# %%
g.setup_logging(fp=fp_log, level=logging.INFO)
c.set_loc(f"{loc}/intermediate")


# %%
from climate.eia import process as p

# %%
genfuel = p.GenFuel(loc=loc)


# %%
genfuel.plant_geo.gdf_nyc.head()

# %%
genfuel.save()