# tools for working with eia data
from climate.eia import specs as s
import requests
from bs4 import BeautifulSoup
import os
import time
import zipfile
from tqdm import tqdm
import pandas as pd
import geopandas as gpd
import glob
import json
from pygsutils import general as g


def get_zip_links():
    with requests.get("https://www.eia.gov/electricity/data/eia923/") as r:
        eia = r.text
    soup = BeautifulSoup(eia, features="html.parser")

    rows = soup.find_all(name="td")
    links_in_rows = [a for r in rows for a in r.find_all(name="a")]
    return [z for z in [l.get("href") for l in links_in_rows] if "zip" in z]


def download_zip(
    filepath, dest_folder, url_start=r"https://www.eia.gov/electricity/data/eia923"
):
    filename = filepath.split("/")[-1]
    with requests.get(f"{url_start}/{filepath}") as r:
        with open(f"{dest_folder}/{filename}", "wb") as f:
            f.write(r.content)


def extract_zip(path_to_zip, dest_folder):
    filename = path_to_zip.split("/")[-1]
    foldername = filename.split(".")[0]
    folderpath = f"{dest_folder}/{foldername}"
    if not os.path.exists(folderpath):
        os.makedirs(folderpath)
    with zipfile.ZipFile(f"./../data/eia/originals/{filename}", "r") as zip_ref:
        zip_ref.extractall(folderpath)


def pull_data(dest_folder):
    zips = get_zip_links()
    g.make_dir(f"{dest_folder}/originals")
    for z in tqdm(zips):
        filename = z.split("/")[-1]
        foldername = filename.split(".")[0]
        download_zip(z, f"{dest_folder}/originals")
        g.make_dir(f"{dest_folder}/extracted/{foldername}")
        extract_zip(
            path_to_zip=f"{dest_folder}/originals/{filename}",
            dest_folder=f"{dest_folder}/extracted/{foldername}",
        )


def fmt_field_names(df):
    def fmt_field_name(name):
        return name.replace("\n", "_").replace(" ", "_").lower()

    return df.rename(columns={f: fmt_field_name(f) for f in df.columns})


def read_json(fp):
    with open(fp, "r") as f:
        contents = f.contents
    return json.loads(contents)


def get_gen_fp(dest_folder, year):
    data_folder = f"{dest_folder}/extracted/f923_{year}/f923_{year}"
    gen_fp = glob.glob(f"{data_folder}/EIA923_Schedules_2_3_4_5_M_*.xlsx")
    assert len(gen_fp) == 1
    return gen_fp[0]


def nonnull_unq_str(l):
    return "|".join(set([str(i) for i in l if not l is None]))


def pull_plant_shapefile(dest_folder):
    download_zip(
        filepath="maps/map_data/PowerPlants_US_EIA.zip",
        dest_folder=f"{dest_folder}/originals",
        url_start="https://www.eia.gov",
    )
    g.make_dir(f"{dest_folder}/extracted/PowerPlants_US_EIA")
    extract_zip(
        path_to_zip=f"{dest_folder}/originals/PowerPlants_US_EIA.zip",
        dest_folder=f"{dest_folder}/extracted/PowerPlants_US_EIA",
    )


def add_sector_desc(df):
    return df.merge(
        right=pd.DataFrame(s.eia_sectors).rename(
            columns={
                "num": "eia_sector_number",
                "desc": "eia_sector_desc",
                "long_desc": "eia_sector_long_desc",
            }
        ),
        on=["eia_sector_number"],
        how="left",
        validate="many_to_one",
    )


def get_plant_geo(dest_folder):
    return gpd.read_file(
        f"{dest_folder}/extracted/PowerPlants_US_EIA/PowerPlants_US_EIA/PowerPlants_US_202004.shp"
    )


def get_nyc_plants(dest_folder):
    plant_gdf = get_plant_geo(dest_folder)
    nyc_plant_gdf = plant_gdf[
        (plant_gdf.StateName == "New York")
        & (
            plant_gdf.County.map(
                lambda x: x is not None and x.lower() in s.nyc_counties
            )
        )
    ]
    return nyc_plant_gdf


def add_nyc_flag(df, dest_folder):
    return df.merge(
        right=get_nyc_plants(dest_folder)[["Plant_Code"]]
        .rename(columns={"Plant_Code": "plant_id"})
        .assign(nyc=1),
        on=["plant_id"],
        how="left",
        validate="many_to_one",
    ).fillna(value={"nyc": 0})


def add_county(df, dest_folder):
    return df.merge(
        right=get_plant_geo(dest_folder)[["Plant_Code", "County"]].rename(
            columns={"Plant_Code": "plant_id"}
        ),
        on=["plant_id"],
        how="left",
        validate="many_to_one",
    ).rename(columns={"County": "county"})


def add_borough(df, dest_folder):
    df_with_county = add_county(df, dest_folder)
    df_with_county["county"] = df_with_county["county"].str.lower()
    return df_with_county.merge(
        right=pd.DataFrame(s.nyc_boroughs),
        on="county",
        how="left",
        validate="many_to_one",
    )


def apply_funcs(ob, funcs):
    for f in funcs:
        ob = f(ob)
    return ob


def highlight_queens(s):
    is_queens = s == "Queens"
    return ["background-color: yellow" if v else "" for v in is_queens]