# tools for working with eia generation data
import calendar
import pandas as pd
from climate.eia import utils as u
from climate.eia import specs as s
from tqdm import tqdm


def get_generation(dest_folder):
    gen_data = []
    gen_specs = s.eia_file_specs["generation"]
    for gs in tqdm(gen_specs):
        year_gen_df = pd.read_excel(
            u.get_gen_fp(dest_folder, gs["year"]),
            sheet_name="Page 4 Generator Data",
            skiprows=gs["start_row"] - 1,
            dtype=object,
        )
        gen_data.append({"year": gs["year"], "df": year_gen_df})
    u.make_dir(f"{dest_folder}/processed")
    return (pd
        .concat([u.fmt_field_names(gd["df"]) for gd in gen_data])
        .to_csv(f"{dest_folder}/processed/generation.csv", index=False)
    )

def get_gen_data(data_folder):
    pass

def long_form(gen_df):
    month_names = [i.lower() for i in calendar.month_name if not i == '']
    month_fields = [f"net_generation_{i}" for i in month_names]
    id_fields = [i for i in gen_df.columns if not i in month_fields]
    melted = pd.melt(
        frame=gen_df,
        id_vars=id_fields,
        value_vars=month_fields,
        var_name="month",
        value_name="net_generation")
    def get_month_as_int(month_field):
        return month_names.index(month_field.split("_")[-1]) + 1
    melted["month_num"] = 12 * melted["year"] + melted["month"].map(get_month_as_int) - 1
    return melted