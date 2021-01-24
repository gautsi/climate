# get eia data
# default: saves to ./../data/eia

# %% tags=['hide-cell']
from IPython import get_ipython

if get_ipython() is not None:
    get_ipython().run_line_magic("load_ext", "autoreload")
    get_ipython().run_line_magic("autoreload", "2")

# %%
from climate.eia import base as b
from pygsutils import general as g

# %%
loc = "./../data/eia"
fp_log = f"{loc}/log_get_eia.log"

# %%
g.setup_logging(fp=fp_log)

# %%
eia = b.EIA(loc=loc)

# %%
eia.download()

# %%
eia.extract()

# %%
# u.pull_plant_shapefile(dest_folder="./../data/eia")

# %%
