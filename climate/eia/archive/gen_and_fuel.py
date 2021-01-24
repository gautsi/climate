# tools for working with EIA generation and fuel data
from climate.eia import utils as u
from climate.eia import specs as s
from tqdm import tqdm
import pandas as pd
import calendar
import datetime as dt

id_fields = [
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


def add_fuel_desc(df):
    return df.merge(
        right=pd.DataFrame(s.aer_fuel_types).rename(
            columns={"code": "aer_fuel_type_code", "desc": "fuel_desc"}
        ),
        on=["aer_fuel_type_code"],
        how="left",
        validate="many_to_one",
    )


def get_gen_and_fuel(dest_folder):
    gf_df = pd.read_csv(f"{dest_folder}/processed/gen_fuel.csv")
    gf_df["netgen"] = gf_df["netgen"].replace(".", "0").astype("float")
    gf_df["gwh"] = gf_df["netgen"] / 1e3
    gf_df["quantity"] = gf_df["quantity"].replace(".", "0").astype("float")
    gf_df["elec_quantity"] = gf_df["elec_quantity"].replace(".", "0").astype("float")
    gf_df["physical_unit_label"] = gf_df["physical_unit_label"].fillna("")
    gf_df["year_month"] = gf_df.apply(
        lambda row: dt.datetime(year=row["year"], month=row["month"], day=1), axis=1
    )
    return gf_df


def pull_gen_and_fuel(dest_folder):
    gen_fuel_data = []
    gen_specs = s.eia_file_specs["gen_and_fuel"]
    for gs in tqdm(gen_specs):
        year_gen_fuel_df = pd.read_excel(
            u.get_gen_fp(dest_folder, gs["year"]),
            sheet_name="Page 1 Generation and Fuel Data",
            skiprows=gs["start_row"] - 1,
            dtype=object,
        )
        gen_fuel_data.append({"year": gs["year"], "df": year_gen_fuel_df})
    u.make_dir(f"{dest_folder}/processed")
    comb = pd.concat([u.fmt_field_names(gd["df"]) for gd in gen_fuel_data])
    lng_form = get_long_form(comb)
    lng_form.to_csv(f"{dest_folder}/processed/gen_fuel.csv", index=False)


def add_orig_fields(gf_df, fields):
    def _(df):
        return df.merge(
            right=gf_df.groupby(id_fields, as_index=False).agg(
                {f: u.nonnull_unq_str for f in fields}
            ),
            on=id_fields,
            how="left",
            validate="many_to_one",
        )

    return _


def get_long_form(gf_df):
    # fill in "none" for null values in the ids
    gf_df.fillna(value={c: "None" for c in id_fields}, inplace=True)
    # check id fields uniquely define rows
    assert len(gf_df) == len(gf_df[id_fields].drop_duplicates())

    lng_df = None
    month_field_prefixes = [
        "quantity",
        "elec_quantity",
        "mmbtuper_unit",
        "elec_mmbtu",
        "tot_mmbtu",
        "netgen",
    ]
    month_names = [i.lower() for i in calendar.month_name if not i == ""]
    prefix_specs = [
        {"prefix": p, "month_fields": [f"{p}_{i}" for i in month_names]}
        for p in month_field_prefixes
    ]

    def get_month_as_int(month_field):
        return month_names.index(month_field.split("_")[-1]) + 1

    def melt_prefix(prefix_spec):
        melted = pd.melt(
            frame=gf_df,
            id_vars=id_fields,
            value_vars=prefix_spec["month_fields"],
            var_name="month",
            value_name=prefix_spec["prefix"],
        )
        melted["month"] = melted["month"].map(get_month_as_int)
        return melted

    for prefix_spec in tqdm(prefix_specs):
        if lng_df is None:
            lng_df = melt_prefix(prefix_spec)
        else:
            lng_df = lng_df.merge(
                right=melt_prefix(prefix_spec),
                on=id_fields + ["month"],
                how="left",
                validate="one_to_one",
            )
    return u.apply_funcs(
        ob=lng_df,
        funcs=[
            add_orig_fields(
                gf_df=gf_df,
                fields=[
                    "plant_name",
                    "operator_name",
                    "aer_fuel_type_code",
                    "physical_unit_label",
                ],
            ),
            add_fuel_desc,
        ],
    )


def get_queens_top_plants(dest_folder):
    gf_df = get_gen_and_fuel(dest_folder=dest_folder)
    nyc_gf_df = u.add_nyc_flag(gf_df, dest_folder=dest_folder).query("nyc == 1")
    nyc_gf_df_w_borough = u.add_borough(nyc_gf_df, dest_folder=dest_folder)
    nyc_plants = nyc_gf_df_w_borough.groupby(
        ["plant_id", "plant_name", "operator_name", "borough"], as_index=False
    ).agg({"gwh": "sum"})
    nyc_top_plants = nyc_plants.sort_values("gwh", ascending=False).iloc[:10]
    return nyc_top_plants.query("borough == 'Queens'").to_dict(orient="records")