# %% [markdown]
"""
# EIA data: exploring
"""

# %%
from IPython import get_ipython
if get_ipython() is not None:
    get_ipython().run_line_magic('load_ext', 'autoreload')
    get_ipython().run_line_magic('autoreload', '2')


# %%
from climate.eia import utils as u
from climate.eia import generation as g
import pandas as pd
data_path = "./../../data/eia"

# %%
gen_data = pd.read_csv(f"{data_path}/processed/generation.csv")

# %%
gen_data.head()

# %%
