# tools for working with eia data
import requests
from bs4 import BeautifulSoup
import os
import time
import zipfile
from tqdm import tqdm

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
        extract_zip(path_to_zip=f"{dest_folder}/originals/{filename}", dest_folder=f"{dest_folder}/extracted/{foldername}")
