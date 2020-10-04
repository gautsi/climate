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

# %%
test = pd.read_csv("http://mis.nyiso.com/public/csv/pal/20201003pal.csv")

# %%
test.head()

# %%
test.dtypes

# %%
len(test)

# %%
test["time"] = pd.to_datetime(test["Time Stamp"])

# %%
import matplotlib.pyplot as plt

# %%
fig, ax = plt.subplots()
for n in test.Name.unique():
    rel_df = test[test.Name == n].sort_values("time")
    ax.plot(rel_df.time, rel_df.Load, label=n)
ax.legend()

# %%
