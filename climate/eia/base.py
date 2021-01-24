from pydantic.dataclasses import dataclass
from functools import cached_property
import requests
from bs4 import BeautifulSoup
from typing import List
from pygsutils import general as g

url_prefix = r"https://www.eia.gov/electricity/data/eia923"


@dataclass
class EIAYear:
    loc: str
    url_suffix: str

    @property
    @g.make_dir
    def loc_orig(self) -> str:
        return f"{self.loc}/originals"

    @property
    def url(self) -> str:
        return f"{url_prefix}/{self.url_suffix}"


@dataclass
class EIA:
    loc: str

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