"""analyzing EIA data
"""

from climate.eia import base as b
from functools import cached_property
import pandas as pd
from typing import List, Dict


class GenFuel(b.GenFuel):
    def __init__(self, loc: str):
        super().__init__(loc=loc)

    @cached_property
    def df_nys(self) -> pd.DataFrame:
        return self.df[self.df.plant_state == "NY"]

    @cached_property
    def df_nyc(self) -> pd.DataFrame:
        return self.df.query("nyc == 1")

    @cached_property
    def df_nyc_plants(self) -> pd.DataFrame:
        return self.df_nyc.groupby(
            ["plant_id", "plant_name", "operator_name", "borough"], as_index=False
        ).agg({"gwh": "sum"})

    @cached_property
    def df_nyc_plants_top(self) -> pd.DataFrame:
        return self.df_nyc_plants.sort_values("gwh", ascending=False).iloc[:10]

    @cached_property
    def df_nyc_plants_top_queens(self) -> pd.DataFrame:
        return self.df_nyc_plants_top.query("borough == 'Queens'")

    @cached_property
    def list_nyc_plants_top_queens(self) -> List[Dict]:
        return self.df_nyc_plants_top_queens.to_dict(orient="records")

    @cached_property
    def df_top_queens(self) -> pd.DataFrame:
        return self.df_nyc.merge(
            right=self.df_nyc_plants_top_queens[["plant_id"]],
            on=["plant_id"],
            how="inner",
            validate="many_to_one",
        )