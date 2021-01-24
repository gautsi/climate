from climate.eia import base as b
from functools import cached_property
import requests
from bs4 import BeautifulSoup
from typing import List, TypeVar
from pygsutils import general as g
import logging


class EIAYear(b.EIAYear):
    def __init__(self, eia: TypeVar("EIA"), url_suffix: str):
        super().__init__(eia=eia, url_suffix=url_suffix)

    def download(self) -> None:
        g.download(url=self.url, fp=self.fp_orig)

    def extract(self) -> None:
        g.extract_zip(path_to_zip=self.fp_orig, dest_folder=self.loc_extract)


class EIA(b.EIA):
    def __init__(self, loc: str):
        super().__init__(loc=loc)

    @cached_property
    def years(self) -> List[EIAYear]:
        return [EIAYear(eia=self, url_suffix=i) for i in self.zip_links]

    def download(self) -> None:
        for yr in self.years:
            yr.download()

    def extract(self) -> None:
        for yr in self.years:
            yr.extract()