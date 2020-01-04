from ftplib import FTP
from contextlib import closing
from io import StringIO
import pandas as pd

ghcn_specs = [
    {
        "name": "stations",
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
    {"name": "readme", "file_name": "readme.txt", "desc": "readme"},
]


def get_ghcn_specs(name):
    return [g for g in ghcn_specs if g["name"] == name][0]


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


def get_stations():
    stations = get_ghcn_file("ghcnd-stations.txt")
    stations_field_pos = [
        (field["pos_from"] - 1, field["pos_to"])
        for field in get_ghcn_specs("stations")["field_specs"]
    ]
    stations_field_names = [
        field["field_name"] for field in get_ghcn_specs("stations")["field_specs"]
    ]
    stations_df = pd.read_fwf(
        StringIO(stations), colspecs=stations_field_pos, header=None
    )
    stations_df.columns = stations_field_names
    return stations_df
