from arcgis.gis import GIS
import libarchive.public
import os
import fiona
import geopandas as gpd
import pandas as pd

def get_zones_archive(data_folder_path):
    anon_gis = GIS()
    public_data_item_id = '414d31994ed141f99de84b0d85d1a33a'
    data_item = anon_gis.content.get(public_data_item_id)
    data_item.download(data_folder_path)

def extract_zones_archive(data_folder_path):
    os.mkdir(f"{data_folder_path}/chermann.gdb")
    with libarchive.public.file_reader(f"{data_folder_path}/NYISOZones.sd") as e:
        for entry in e:
            if "chermann.gdb" in entry.pathname:
                with open(f"{data_folder_path}/chermann.gdb/{entry.pathname.split('/')[-1]}", 'wb') as f:
                    for block in entry.get_blocks():
                        f.write(block)

def get_zones(data_folder_path):
    gdb = fiona.open(f"{data_folder_path}/chermann.gdb/")
    return gpd.GeoDataFrame.from_features(gdb)

def get_load(date):
    load = pd.read_csv(f"http://mis.nyiso.com/public/csv/pal/{date.strftime('%Y%m%d')}pal.csv")
    load["time"] = pd.to_datetime(load["Time Stamp"])
    return load