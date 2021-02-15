# get eia data
# default: saves to ./../data/eia

# %% tags=['hide-cell']
from IPython import get_ipython

if get_ipython() is not None:
    get_ipython().run_line_magic("load_ext", "autoreload")
    get_ipython().run_line_magic("autoreload", "2")

# %%
from climate.eia import pull as p
from pygsutils import general as g

# %%
loc = "./../../data/eia"
fp_log = f"{loc}/log_get_eia.log"

# %%
g.setup_logging(fp=fp_log)

# %%
# EIA data
eia = p.EIA(loc=loc)

# %%
eia.download()

# %%
eia.extract()

# %%
# plant geo data
plant_geo = p.PlantGeo(loc=loc)

# %%
plant_geo.download()

# %%
plant_geo.extract()