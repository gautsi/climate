from climate.eia import base as b
from functools import cached_property
from typing import List, TypeVar
from pygsutils import general as g, data as d, cache as c
import logging
import pandas as pd
import calendar
import datetime as dt
import geopandas as gpd


class GenFuelYear(b.GenFuelYear):
    def __init__(self, eia: TypeVar("EIA"), url_suffix: str):
        super().__init__(eia=eia, url_suffix=url_suffix)

    @cached_property
    def df_raw(self) -> pd.DataFrame:
        logging.info(f"reading {self.fp_gen}")
        return pd.read_excel(
            self.fp_gen,
            sheet_name="Page 1 Generation and Fuel Data",
            skiprows=self.start_row_gen - 1,
            dtype=object,
        )

    @cached_property
    def df_fix_fields(self) -> pd.DataFrame:
        return d.fmt_field_names(self.df_raw)


class MonthField(b.MonthField):
    def __init__(self, genfuel: TypeVar("GenFuel"), prefix: str):
        super().__init__(prefix=prefix)
        self.genfuel = genfuel

    @cached_property
    def df_melted(self):
        logging.info(f"melting across months for prefix {self.prefix}")
        melted = pd.melt(
            frame=self.genfuel.df_fillna,
            id_vars=self.genfuel.id_fields,
            value_vars=self.month_fields,
            var_name="month",
            value_name=self.prefix,
        )
        melted["month"] = melted["month"].map(self.get_month_as_int)
        return melted


class GenFuel(b.GenFuel):
    def __init__(self, loc: str):
        super().__init__(loc=loc)
        self.plant_geo = b.PlantGeo(loc=loc)
        self.cache = c.DFCache(loc=f"{self.loc}/intermediate")

    @cached_property
    def years(self) -> List[GenFuelYear]:
        return [GenFuelYear(eia=self, url_suffix=i) for i in self.zip_links]

    def get_df_comb(self) -> pd.DataFrame:
        logging.info("combining gen fuel data across years")
        return pd.concat(
            [yr.df_fix_fields for yr in self.years if yr.year in self.years_to_include]
        )

    @cached_property
    def df_comb(self) -> pd.DataFrame:
        return self.cache.store(name="df_comb")(self.get_df_comb)()

    @property
    def prefixes_fields_month(self) -> List[str]:
        return [
            "quantity",
            "elec_quantity",
            "mmbtuper_unit",
            "elec_mmbtu",
            "tot_mmbtu",
            "netgen",
        ]

    @property
    def month_fields(self) -> List[MonthField]:
        return [MonthField(genfuel=self, prefix=i) for i in self.prefixes_fields_month]

    def get_df_fillna(self) -> pd.DataFrame:
        logging.info("filling in 'None' for null values in the ids")

        df_fillna = self.df_comb.fillna(value={c: "None" for c in self.id_fields})
        # check id fields uniquely define rows
        assert len(df_fillna) == len(df_fillna[self.id_fields].drop_duplicates())
        return df_fillna

    @cached_property
    def df_fillna(self) -> pd.DataFrame:
        return self.cache.store(name="df_fillna")(self.get_df_fillna)()

    def get_df_lng_raw(self) -> pd.DataFrame:
        logging.info("generating long form data")
        df_lng_raw = None
        for month_field in self.month_fields:
            if df_lng_raw is None:
                df_lng_raw = month_field.df_melted
            else:
                df_lng_raw = df_lng_raw.merge(
                    right=month_field.df_melted,
                    on=self.id_fields + ["month"],
                    how="left",
                    validate="one_to_one",
                )
        return df_lng_raw

    @cached_property
    def df_lng_raw(self) -> pd.DataFrame:
        return self.cache.store(name="df_lng_raw")(self.get_df_lng_raw)()

    @property
    def fields_orig(self) -> List[str]:
        return [
            "plant_name",
            "operator_name",
            "aer_fuel_type_code",
            "physical_unit_label",
        ]

    def get_df_lng_w_orig(self) -> pd.DataFrame:
        return self.df_lng_raw.merge(
            right=self.df_fillna.groupby(self.id_fields, as_index=False).agg(
                {f: d.nonnull_unq_str for f in self.fields_orig}
            ),
            on=self.id_fields,
            how="left",
            validate="many_to_one",
        )

    @cached_property
    def df_lng_w_orig(self) -> pd.DataFrame:
        return self.cache.store(name="df_lng_w_orig")(self.get_df_lng_w_orig)()

    @property
    def df_fuel_types(self) -> pd.DataFrame:
        df_raw = pd.DataFrame([i.dict() for i in b.fuel_types])
        df_raw["general"] = df_raw["general"].map(lambda x: x["name"])
        return df_raw.rename(
            columns={
                "code": "aer_fuel_type_code",
                "desc": "fuel_desc",
                "general": "general_fuel_type",
            }
        )

    def get_df_w_fuel_desc(self) -> pd.DataFrame:
        logging.info("adding fuel desc")
        return self.df_lng_w_orig.merge(
            right=self.df_fuel_types,
            on=["aer_fuel_type_code"],
            how="left",
            validate="many_to_one",
        )

    @cached_property
    def df_w_fuel_desc(self) -> pd.DataFrame:
        return self.cache.store(name="df_w_fuel_desc")(self.get_df_w_fuel_desc)()

    def get_df_replace_periods(self) -> pd.DataFrame:
        logging.info("replacing periods with zeros")
        for field in self.prefixes_fields_month:
            self.df_w_fuel_desc[field] = (
                self.df_w_fuel_desc[field].replace(".", "0").astype("float")
            )
        return self.df_w_fuel_desc

    @cached_property
    def df_replace_periods(self) -> pd.DataFrame:
        return self.cache.store(name="df_replace_periods")(
            self.get_df_replace_periods
        )()

    def get_df_nyc_flag(self) -> pd.DataFrame:
        logging.info("adding nyc flag")
        return self.df_replace_periods.merge(
            right=self.plant_geo.gdf_nyc[["Plant_Code"]]
            .rename(columns={"Plant_Code": "plant_id"})
            .assign(nyc=1),
            on=["plant_id"],
            how="left",
            validate="many_to_one",
        ).fillna(value={"nyc": 0})

    @cached_property
    def df_nyc_flag(self) -> pd.DataFrame:
        return self.cache.store(name="df_nyc_flag")(self.get_df_nyc_flag)()

    @cached_property
    def df_w_county(self) -> pd.DataFrame:
        logging.info("adding county")
        return self.df_nyc_flag.merge(
            right=self.plant_geo.gdf[["Plant_Code", "County"]].rename(
                columns={"Plant_Code": "plant_id"}
            ),
            on=["plant_id"],
            how="left",
            validate="many_to_one",
        ).rename(columns={"County": "county"})

    @cached_property
    def df_w_borough(self) -> pd.DataFrame:
        logging.info("adding borough name")
        df_boroughs = pd.DataFrame(
            [{"county": i.value.county, "borough": i.value.name} for i in b.NYCBoroughs]
        )
        self.df_w_county["county"] = self.df_w_county["county"].str.lower()
        return self.df_w_county.merge(
            right=df_boroughs,
            on=["county"],
            how="left",
            validate="many_to_one",
        )

    @cached_property
    def df(self) -> pd.DataFrame:
        logging.info("last processing steps")
        df = self.df_w_borough
        df["gwh"] = df["netgen"] / 1e3
        df["physical_unit_label"] = df["physical_unit_label"].fillna("")
        df["year_month"] = df.apply(
            lambda row: dt.datetime(year=row["year"], month=row["month"], day=1), axis=1
        )
        return df

    def save(self) -> None:
        logging.info(f"saving to {self.fp}")
        self.df.to_csv(self.fp, index=False)