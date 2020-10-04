# checking zones download
# %%
from IPython import get_ipython
if get_ipython() is not None:
    get_ipython().run_line_magic('load_ext', 'autoreload')
    get_ipython().run_line_magic('autoreload', '2')

# %%
from climate.nyiso import utils as u

# %%
dfp = "./../data"

# %%
u.get_zones_archive(dfp)

# %%
u.extract_zones_archive(dfp)

# %%
