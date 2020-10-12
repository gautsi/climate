# get eia data
# default: saves to ./../data/eia
# %%
from climate.eia import utils as u

# %%
u.pull_data(dest_folder="./../data/eia")

# %%
u.pull_plant_shapefile(dest_folder="./../data/eia")

# %%
