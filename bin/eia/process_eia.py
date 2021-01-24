# process eia data

# %% tags=['hide-cell']
from IPython import get_ipython

if get_ipython() is not None:
    get_ipython().run_line_magic("load_ext", "autoreload")
    get_ipython().run_line_magic("autoreload", "2")

# %%
from climate.eia import process as p
from pygsutils import general as g

# %%
loc = "./../../data/eia"
fp_log = f"{loc}/log_process_eia.log"

# %%
g.setup_logging(fp=fp_log)

# %%
genfuel = p.GenFuel(loc=loc)

# %%
genfuel.save()