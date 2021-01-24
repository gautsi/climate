from climate.eia import base as b
from functools import cached_property
from typing import List, TypeVar
from pygsutils import general as g
from pygsutils import data as d
import logging
import pandas as pd
import calendar


class GenFuelYear(b.EIAYear):
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


class MonthField:
    def __init__(self, genfuel: TypeVar("GenFuel"), prefix: str):
        self.genfuel = genfuel
        self.prefix = prefix

    @property
    def month_names(self) -> List[str]:
        return [i.lower() for i in calendar.month_name if not i == ""]

    def get_month_as_int(self, field: str) -> int:
        return self.month_names.index(field.split("_")[-1]) + 1

    @property
    def month_fields(self) -> List[str]:
        return [f"{self.prefix}_{i}" for i in self.month_names]

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


class GenFuel(b.EIA):
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

    @cached_property
    def df_comb(self) -> pd.DataFrame:
        logging.info("combining gen fuel data across years")
        return pd.concat(
            [yr.df_fix_fields for yr in self.years if yr.year in self.years_to_include]
        )

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

    @cached_property
    def df_fillna(self) -> pd.DataFrame:
        logging.info("filling in 'None' for null values in the ids")
        df_fillna = self.df_comb.fillna(value={c: "None" for c in self.id_fields})
        # check id fields uniquely define rows
        assert len(df_fillna) == len(df_fillna[self.id_fields].drop_duplicates())
        return df_fillna

    @cached_property
    def df_lng_raw(self) -> pd.DataFrame:
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

    @property
    def fields_orig(self) -> List[str]:
        return [
            "plant_name",
            "operator_name",
            "aer_fuel_type_code",
            "physical_unit_label",
        ]

    @cached_property
    def df_lng_w_orig(self) -> pd.DataFrame:
        return self.df_lng_raw.merge(
            right=self.df_fillna.groupby(self.id_fields, as_index=False).agg(
                {f: d.nonnull_unq_str for f in self.fields_orig}
            ),
            on=self.id_fields,
            how="left",
            validate="many_to_one",
        )

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

    @cached_property
    def df_w_fuel_desc(self) -> pd.DataFrame:
        logging.info("adding fuel desc")
        return self.df_lng_w_orig.merge(
            right=self.df_fuel_types,
            on=["aer_fuel_type_code"],
            how="left",
            validate="many_to_one",
        )