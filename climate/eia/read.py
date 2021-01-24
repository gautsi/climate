from climate.eia import process as p
import pandas as pd
from functools import cached_property

class GenFuel(p.GenFuel):
    def __init__(self, loc: str):
        super().__init__(loc=loc)

    @cached_property
    def df(self) -> pd.DataFrame:
        return pd.read_csv(self.fp)
