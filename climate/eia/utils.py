# tools for working with eia data
import requests
from bs4 import BeautifulSoup
import os
import time
import zipfile
from tqdm import tqdm
import pandas as pd
import glob
import json

eia_file_specs = {
    "generation": [{"year": 2020, "start_row": 5}, {"year": 2019, "start_row": 6}]
}


def get_zip_links():
    with requests.get("https://www.eia.gov/electricity/data/eia923/") as r:
        eia = r.text
    soup = BeautifulSoup(eia, features="html.parser")

    rows = soup.find_all(name="td")
    links_in_rows = [a for r in rows for a in r.find_all(name="a")]
    return [z for z in [l.get("href") for l in links_in_rows] if "zip" in z]


def download_zip(z, dest_folder):
    filename = z.split("/")[-1]
    url_start = r"https://www.eia.gov/electricity/data/eia923/"
    with requests.get(f"{url_start}{z}") as r:
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


def make_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def pull_data(dest_folder):
    zips = get_zip_links()
    make_dir(f"{dest_folder}/originals")
    for z in tqdm(zips):
        filename = z.split("/")[-1]
        foldername = filename.split(".")[0]
        download_zip(z, f"{dest_folder}/originals")
        make_dir(f"{dest_folder}/extracted/{foldername}")
        extract_zip(
            path_to_zip=f"{dest_folder}/originals/{filename}",
            dest_folder=f"{dest_folder}/extracted/{foldername}",
        )


def get_gen_fp(dest_folder, year):
    data_folder = f"{dest_folder}/extracted/f923_{year}/f923_{year}"
    gen_fp = glob.glob(f"{data_folder}/EIA923_Schedules_2_3_4_5_M_*.xlsx")
    assert len(gen_fp) == 1
    return gen_fp[0]


def fmt_field_names(df):
    def fmt_field_name(name):
        return name.replace("\n", "_").replace(" ", "_").lower()

    return df.rename(columns={f: fmt_field_name(f) for f in df.columns})


def read_json(fp):
    with open(fp, "r") as f:
        contents = f.contents
    return json.loads(contents)


def get_generation(dest_folder):
    gen_data = []
    gen_specs = eia_file_specs["generation"]
    for gs in tqdm(gen_specs):
        year_gen_df = pd.read_excel(
            get_gen_fp(dest_folder, gs["year"]),
            sheet_name="Page 4 Generator Data",
            skiprows=gs["start_row"] - 1,
            dtype=object,
        )
        gen_data.append({"year": gs["year"], "df": year_gen_df})
    make_dir(f"{dest_folder}/processed")
    return (pd
        .concat([fmt_field_names(gd["df"]) for gd in gen_data])
        .to_csv(f"{dest_folder}/processed/generation.csv", index=False)
    )