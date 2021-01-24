from pydantic.dataclasses import dataclass
from functools import cached_property
import requests
from bs4 import BeautifulSoup
from typing import List, TypeVar
from pygsutils import general as g
import logging

url_prefix = r"https://www.eia.gov/electricity/data/eia923"


@dataclass
class EIAYear:
    eia: TypeVar("EIA")
    url_suffix: str

    @property
    def url(self) -> str:
        return f"{url_prefix}/{self.url_suffix}"

    @property
    def filename(self) -> str:
        return self.url_suffix.split("/")[-1]

    @property
    def foldername(self) -> str:
        return self.filename.split(".")[0]

    @property
    def fp_orig(self) -> str:
        return f"{self.eia.loc_orig}/{self.filename}"

    @property
    def loc_extract(self) -> str:
        return f"{self.eia.loc_extract}/{self.foldername}"

    def download(self) -> None:
        g.download(url=self.url, fp=self.fp_orig)

    def extract(self) -> None:
        g.extract_zip(path_to_zip=self.fp_orig, dest_folder=self.loc_extract)


@dataclass
class EIA:
    loc: str

    @property
    @g.make_dir
    def loc_orig(self) -> str:
        return f"{self.loc}/originals"

    @property
    @g.make_dir
    def loc_extract(self) -> str:
        return f"{self.loc}/extracted"

    @cached_property
    def home_html(self) -> str:
        with requests.get("https://www.eia.gov/electricity/data/eia923/") as r:
            text = r.text
        return text

    @cached_property
    def home_soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.home_html, features="html.parser")

    @cached_property
    def zip_links(self) -> List[str]:
        rows = self.home_soup.find_all(name="td")
        links_in_rows = [a for r in rows for a in r.find_all(name="a")]
        links = []
        for l in links_in_rows:
            href = l.get("href")
            if "zip" in href:
                links.append(href)
        return links

    @cached_property
    def years(self) -> List[EIAYear]:
        return [EIAYear(eia=self, url_suffix=i) for i in self.zip_links]

    def download(self) -> None:
        for yr in self.years:
            yr.download()

    def extract(self) -> None:
        for yr in self.years:
            yr.extract()