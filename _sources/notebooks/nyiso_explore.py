# %% [markdown]
"""
# NYISO data: exploring
Exploring NYISO data, in particular electric consumption fuel mix over time
"""

# %% tags=['hide-cell']
from IPython import get_ipython
if get_ipython() is not None:
    get_ipython().run_line_magic('load_ext', 'autoreload')
    get_ipython().run_line_magic('autoreload', '2')

# %%
from climate.nyiso import utils as u
import logging
from pygsutils import general as g

# %%
dfp = "./../data"

log_fp = "./../logs/get_nyiso.log"

# %%
g.setup_logging(log_fp)


# %%
fm = u.get_fuel_mix(data_folder_path=dfp)

# %%
len(fm)

# %%
fm.info()

# %%
fm.head()

# %%
