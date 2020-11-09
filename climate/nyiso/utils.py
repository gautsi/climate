from arcgis.gis import GIS
import libarchive.public
import os
import fiona
import geopandas as gpd
import pandas as pd
import logging
import requests
from bs4 import BeautifulSoup
from pygsutils import general as g
import glob


def get_zones_archive(data_folder_path):
    anon_gis = GIS()
    public_data_item_id = "414d31994ed141f99de84b0d85d1a33a"
    data_item = anon_gis.content.get(public_data_item_id)
    logging.info(f"Saving zones archive to {data_folder_path}")
    data_item.download(data_folder_path)


def extract_zones_archive(data_folder_path):
    logging.info(f"Extracting zones archive to {data_folder_path}/chermann.gdb")
    os.mkdir(f"{data_folder_path}/chermann.gdb")
    with libarchive.public.file_reader(f"{data_folder_path}/NYISOZones.sd") as e:
        for entry in e:
            if "chermann.gdb" in entry.pathname:
                with open(
                    f"{data_folder_path}/chermann.gdb/{entry.pathname.split('/')[-1]}",
                    "wb",
                ) as f:
                    for block in entry.get_blocks():
                        f.write(block)


def get_zones(data_folder_path):
    gdb = fiona.open(f"{data_folder_path}/chermann.gdb/")
    return gpd.GeoDataFrame.from_features(gdb)


def get_load(date):
    load = pd.read_csv(
        f"http://mis.nyiso.com/public/csv/pal/{date.strftime('%Y%m%d')}pal.csv"
    )
    load["time"] = pd.to_datetime(load["Time Stamp"])
    return load


def download_fuel_mix(data_folder_path: str) -> None:
    data_loc = f"{data_folder_path}/nyiso/fuel_mix"
    logging.info(f"Downloading NYISO fuel mix data to {data_loc}")
    os.makedirs(data_loc)
    site = "http://mis.nyiso.com/public/P-63list.htm"
    logging.info(f"Grabbing links from site {site}")
    with requests.get(site) as r:
        fm = r.text
    soup = BeautifulSoup(fm, features="html.parser")
    links = [l.get("href") for l in soup.find_all(name="a") if "zip" in l.get("href")]
    num_links = len(links)
    url_start = "http://mis.nyiso.com/public/"
    for i, l in enumerate(links):
        logging.info(f"Downloading {i + 1} out of {num_links} zips")
        fn = l.split("/")[-1]
        g.download(url=f"{url_start}/{l}", fp=f"{data_loc}/{fn}")


def extract_fuel_mix(data_folder_path: str) -> None:
    data_loc = f"{data_folder_path}/nyiso/fuel_mix"
    zip_fps = glob.glob(f"{data_loc}/*.zip")
    for i, z in enumerate(zip_fps):
        logging.info(f"Extracting {i+1} of {len(zip_fps)} fuel mix zips: {z}")
        g.extract_zip(path_to_zip=z, dest_folder=f"{data_loc}/extracts")


def combine_fuel_mix(data_folder_path: str) -> None:
    data_loc = f"{data_folder_path}/nyiso/fuel_mix"
    csv_locs = glob.glob(f"{data_loc}/extracts/**/*.csv", recursive=True)
    dfs = []
    for i, fp in enumerate(csv_locs):
        logging.info(f"Reading {i+1} of {len(csv_locs)} fuel mix csvs")
        dfs.append(pd.read_csv(fp))
    comb_loc = f"{data_loc}/combined"
    os.makedirs(comb_loc)
    comb_fp = f"{comb_loc}/comb_fuel_mix.csv"
    logging.info(f"Saving combined fuel mix data to {comb_fp}")
    pd.concat(dfs).to_csv(comb_fp, index=False)


def get_fuel_mix(data_folder_path: str) -> None:
    return pd.read_csv(f"{data_folder_path}/nyiso/fuel_mix/combined/comb_fuel_mix.csv")