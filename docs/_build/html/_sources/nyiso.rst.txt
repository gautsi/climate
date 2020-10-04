*********
NYISO
*********

.. jupyter-kernel:: .venv



Objective
=========

To pull energy mix data for NYS from NYISO and check trends for carbon and non-carbon sources aound the state.


Data
========

Zone shapefiles
---------------

From https://www.arcgis.com/home/item.html?id=414d31994ed141f99de84b0d85d1a33a.

To pull from source into a GeoDataFrame:

.. code-block:: python

    from climate.nyiso import utils as u
    data_folder_path = "./data/"
    u.get_zones_archive(data_folder_path=data_folder_path)
    u.extract_zones_archive(data_folder_path=data_folder_path)
    zones = get_zones(data_folder_path=data_folder_path)


.. jupyter-execute::

    import pandas as pd
    df = pd.DataFrame({"a": [1, 2, 4], "b": [4, 5, 6]})
    df