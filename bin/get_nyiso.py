# script to pull NYISO data

# %% tags=["hide-cell"]
from IPython import get_ipython
if get_ipython() is not None:
    get_ipython().run_line_magic('load_ext', 'autoreload')
    get_ipython().run_line_magic('autoreload', '2')

# %%
from climate.nyiso import utils as u
import logging
from pygsutils import general as g
import requests
from bs4 import BeautifulSoup

# %%
dfp = "./../data"

log_fp = "./../logs/get_nyiso.log"

# %%
g.setup_logging(log_fp)

# %%
# zone shapefiles
u.get_zones_archive(dfp)

u.extract_zones_archive(dfp)

# %%
# fuel mix
u.download_fuel_mix(data_folder_path=dfp)

# %%
u.extract_fuel_mix(data_folder_path=dfp)

# %%
u.combine_fuel_mix(data_folder_path=dfp)

# %%
u.process_fuel_mix(data_folder_path=dfp)

# %%
u.aggregate_fuel_mix(data_folder_path=dfp)

# %%
