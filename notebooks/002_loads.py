# check pulling load data from nyiso

# %%
from IPython import get_ipython
if get_ipython() is not None:
    get_ipython().run_line_magic('load_ext', 'autoreload')
    get_ipython().run_line_magic('autoreload', '2')

# %%
from climate.nyiso import utils as u

# %%
import pandas as pd
import datetime as dt

# %%
date = dt.datetime(year=2020, month=10, day=3)


# %%

# %%
test = u.get_load(date)

# %%
test.head()

# %%
test.dtypes

# %%
len(test)


# %%
import matplotlib.pyplot as plt

# %%
fig, ax = plt.subplots()
for n in test.Name.unique():
    rel_df = test[test.Name == n].sort_values("time")
    ax.plot(rel_df.time, rel_df.Load, label=n)
ax.legend()

# %%
