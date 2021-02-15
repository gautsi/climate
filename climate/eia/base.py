from functools import cached_property
import requests
from bs4 import BeautifulSoup
from typing import List, TypeVar, Optional
from pygsutils import general as g
import logging
import glob
from pydantic import BaseModel
from dataclasses import dataclass
import calendar
import pandas as pd
import geopandas as gpd
from enum import Enum


class EIAYear:
    def __init__(self, eia: TypeVar("EIA"), url_suffix: str):
        self.eia = eia
        self.url_suffix = url_suffix

    @property
    def url(self) -> str:
        url_prefix = r"https://www.eia.gov/electricity/data/eia923"
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

    @property
    def year(self) -> Optional[int]:
        try:
            year = int(self.loc_extract.split("_")[-1])
        except ValueError:
            logging.info(f"could not get year for {self.loc_extract}")
            year = None
        return year

    @property
    def fp_gen(self) -> str:
        fn_prefix = r"EIA923_Schedules_2_3_4_5_M_"
        pos_fp = glob.glob(f"{self.loc_extract}/{fn_prefix}*.xlsx")
        assert (
            len(pos_fp) == 1
        ), f"too many possible filepaths for generation data for {self.year}"
        return pos_fp[0]

    @property
    def start_row_gen(self) -> int:
        if self.year in [2016, 2017, 2018, 2019, 2020]:
            return 6
        else:
            raise (f"data for year {self.year} has not been checked yet")


class EIA:
    def __init__(self, loc: str):
        self.loc = loc

    @property
    @g.make_dir
    def loc_orig(self) -> str:
        return f"{self.loc}/originals"

    @property
    @g.make_dir
    def loc_extract(self) -> str:
        return f"{self.loc}/extracted"

    @property
    @g.make_dir
    def loc_processed(self) -> str:
        return f"{self.loc}/processed"

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


class GeneralFuelType(BaseModel):
    name: str


fossil_fuel = GeneralFuelType(name="fossil_fuel")
nuclear = GeneralFuelType(name="nuclear")
renewable = GeneralFuelType(name="renewable")


class FuelType(BaseModel):
    code: str
    desc: str
    general: GeneralFuelType
    renew: bool


fuel_types = [
    FuelType(code="SUN", desc="Solar PV and thermal", renew=True, general=renewable),
    FuelType(code="COL", desc="Coal ", renew=False, general=fossil_fuel),
    FuelType(code="DFO", desc="Distillate Petroleum", renew=False, general=fossil_fuel),
    FuelType(code="GEO", desc="Geothermal", renew=True, general=renewable),
    FuelType(
        code="HPS", desc="Hydroelectric Pumped Storage", renew=True, general=renewable
    ),
    FuelType(
        code="HYC", desc="Hydroelectric Conventional", renew=True, general=renewable
    ),
    FuelType(
        code="MLG",
        desc="Biogenic Municipal Solid Waste and Landfill Gas",
        renew=True,
        general=renewable,
    ),
    FuelType(code="NG", desc="Natural Gas", renew=False, general=fossil_fuel),
    FuelType(code="NUC", desc="Nuclear", renew=False, general=nuclear),
    FuelType(code="OOG", desc="Other Gases", renew=False, general=fossil_fuel),
    FuelType(code="ORW", desc="OtherRenewables ", renew=True, general=renewable),
    FuelType(
        code="OTH",
        desc="Other (including nonbiogenic MSW)",
        renew=False,
        general=fossil_fuel,
    ),
    FuelType(code="PC", desc="Petroleum Coke", renew=False, general=fossil_fuel),
    FuelType(code="RFO", desc="Residual Petroleum", renew=False, general=fossil_fuel),
    FuelType(code="WND", desc="Wind", renew=True, general=renewable),
    FuelType(code="WOC", desc="Waste Coal", renew=False, general=fossil_fuel),
    FuelType(code="WOO", desc="Waste Oil", renew=False, general=fossil_fuel),
    FuelType(code="WWW", desc="Wood and Wood Waste", renew=True, general=renewable),
]


class GenFuelYear(EIAYear):
    def __init__(self, eia: TypeVar("EIA"), url_suffix: str):
        super().__init__(eia=eia, url_suffix=url_suffix)


class MonthField:
    def __init__(self, prefix: str):
        self.prefix = prefix

    @property
    def month_names(self) -> List[str]:
        return [i.lower() for i in calendar.month_name if not i == ""]

    def get_month_as_int(self, field: str) -> int:
        return self.month_names.index(field.split("_")[-1]) + 1

    @property
    def month_fields(self) -> List[str]:
        return [f"{self.prefix}_{i}" for i in self.month_names]


class GenFuel(EIA):
    def __init__(self, loc: str):
        super().__init__(loc=loc)

    @cached_property
    def years(self) -> List[GenFuelYear]:
        return [GenFuelYear(eia=self, url_suffix=i) for i in self.zip_links]

    @cached_property
    def years_to_include(self) -> List[int]:
        return [2020, 2019, 2018, 2017, 2016]

    @property
    def fp(self) -> str:
        return f"{self.loc_processed}/gen_fuel.csv"

    @property
    def id_fields(self) -> List[str]:
        return [
            "plant_id",
            "combined_heat_and_power_plant",
            "nuclear_unit_id",
            "operator_id",
            "naics_code",
            "plant_state",
            "eia_sector_number",
            "reported_prime_mover",
            "reported_fuel_type_code",
            "year",
        ]

    @cached_property
    def df(self) -> pd.DataFrame:
        return pd.read_csv(self.fp)


@dataclass
class NYCBorough:
    name: str
    county: str


class NYCBoroughs(Enum):
    MANHATTAN = NYCBorough(name="Manhattan", county="new york")
    BROOKLYN = NYCBorough(name="Brooklyn", county="kings")
    QUEENS = NYCBorough(name="Queens", county="queens")
    STATENISLAND = NYCBorough(name="Staten Island", county="richmond")
    BRONX = NYCBorough(name="Bronx", county="bronx")


class PlantGeo:
    def __init__(self, loc: str):
        self.loc = loc

    @property  # type: ignore
    @g.make_dir
    def loc_orig(self) -> str:
        return f"{self.loc}/originals"

    @property  # type: ignore
    @g.make_dir
    def loc_extract(self) -> str:
        return f"{self.loc}/extracted/PowerPlants_US_EIA"

    @property
    def fp_shp(self) -> str:
        return f"{self.loc_extract}/PowerPlants_US_EIA/PowerPlants_US_202004.shp"

    @cached_property
    def gdf(self) -> gpd.GeoDataFrame:
        return gpd.read_file(self.fp_shp)

    @cached_property
    def gdf_nyc(self) -> gpd.GeoDataFrame:
        return self.gdf[
            (self.gdf.StateName == "New York")
            & (
                self.gdf.County.map(
                    lambda x: x is not None
                    and x.lower() in [i.name for i in NYCBoroughs]
                )
            )
        ]
