"""
Functions to read and work with data from GHCN
"""

from ftplib import FTP
from contextlib import closing
from io import StringIO
import pandas as pd
from tqdm import tqdm

# field specifications for fixed-width GHCN files
ghcn_specs = [
    {
        "file_type": "stations",
        "file_name": "ghcnd-stations.txt",
        "desc": "stations",
        "field_specs": [
            {"field_name": "ID", "pos_from": 1, "pos_to": 11},
            {"field_name": "LATITUDE", "pos_from": 13, "pos_to": 20},
            {"field_name": "LONGITUDE", "pos_from": 22, "pos_to": 30},
            {"field_name": "ELEVATION", "pos_from": 32, "pos_to": 37},
            {"field_name": "STATE", "pos_from": 39, "pos_to": 40},
            {"field_name": "NAME", "pos_from": 42, "pos_to": 71},
            {"field_name": "GSN FLAG", "pos_from": 73, "pos_to": 75},
            {"field_name": "HCN/CRN FLAG", "pos_from": 77, "pos_to": 79},
            {"field_name": "WMO ID", "pos_from": 81, "pos_to": 85},
        ],
    },
    {"file_type": "readme", "file_name": "readme.txt", "desc": "readme"},
    {
        "file_type": "station_data",
        "desc": "data for one station (.dly file), see section III of readme",
        "field_specs": [
            {"field_name": "ID", "pos_from": 1, "pos_to": 11},
            {"field_name": "YEAR", "pos_from": 12, "pos_to": 15},
            {"field_name": "MONTH", "pos_from": 16, "pos_to": 17},
            {"field_name": "ELEMENT", "pos_from": 18, "pos_to": 21},
        ]
        + [
            {
                "field_name": "{typ}{day}".format(typ=typ, day=day),
                "pos_from": 14 + 8 * day + (0 if typ_ind == 0 else typ_ind + 4),
                "pos_to": 14 + 8 * day + (typ_ind + 4),
            }
            for typ_ind, typ in enumerate(["VALUE", "MFLAG", "QFLAG", "SFLAG"])
            for day in range(1, 32)
        ],
    },
]


def get_ghcn_specs(file_type="stations"):
    """Gets the field specifications for a given file type
    Args:
        file_type (str): the file type
    Returns:
        dict: the field specifications (see ghcn_specs)
    """

    return [g for g in ghcn_specs if g["file_type"] == file_type][0]


def get_ghcn_file(file_name: str = "ghcnd-stations.txt"):
    file = ""
    with closing(FTP("ftp.ncdc.noaa.gov")) as ftp:
        ftp.login()
        with closing(StringIO()) as r:
            # need to add newlines, hence custom call back
            ftp.retrlines(
                "RETR /pub/data/ghcn/daily/{file_name}".format(file_name=file_name),
                callback=lambda line: r.write(line + "\n"),
            )
            file = r.getvalue()
    return file


def read_fwf(file_name: str = "ghcnd-stations.txt", file_type: str = "stations"):
    file = get_ghcn_file(file_name)
    field_pos = [
        (field["pos_from"] - 1, field["pos_to"])
        for field in get_ghcn_specs(file_type)["field_specs"]
    ]
    field_names = [
        field["field_name"] for field in get_ghcn_specs(file_type)["field_specs"]
    ]
    df = pd.read_fwf(StringIO(file), colspecs=field_pos, header=None)
    df.columns = field_names
    return df


def get_stations():
    return read_fwf(file_name="ghcnd-stations.txt", file_type="stations")


def get_station_data(station_id: str = "USW00014771"):
    return read_fwf(file_name="all/{}.dly".format(station_id), file_type="station_data")


def c_to_f(c):
    """
    tenths of degrees Celsius to Fahrenheit
    """
    return (c * 9.0 / 50.0) + 32


def get_temps(station_data):
    temps = pd.melt(
        frame=station_data[station_data.ELEMENT.isin(["TMAX", "TMIN"])],
        id_vars=["ID", "YEAR", "MONTH", "ELEMENT"],
        value_vars=["VALUE{}".format(day) for day in range(1, 32)],
        var_name="var",
        value_name="temp_c",
    ).query("temp_c != -9999")

    temps["day"] = temps["var"].map(lambda x: x[5:])
    temps["temp_f"] = temps["temp_c"].map(c_to_f)
    temps["date"] = pd.to_datetime(temps[["YEAR", "MONTH", "day"]])
    return temps


def get_all_temps(limit=None, use_tqdm=False):

    # get station data
    stations_df = get_stations()

    # get station ids for the stations with GSN data
    gcn_station_specs = [
        {"station_id": station_id}
        for station_id in stations_df[pd.notnull(stations_df["GSN FLAG"])].ID.unique()
    ][:limit]

    def tqdm_wrap(l):
        return tqdm(l) if use_tqdm else l

    # get full data for each station
    for station_spec in tqdm_wrap(gcn_station_specs):
        station_spec["station_data"] = get_station_data(
            station_id=station_spec["station_id"]
        )
        # pull temperatures from full data
        station_spec["temps"] = get_temps(station_spec["station_data"])

    return pd.concat([s["temps"] for s in gcn_station_specs])
