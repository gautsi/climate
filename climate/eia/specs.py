# specifications

eia_file_specs = {
    "generation": [{"year": 2020, "start_row": 5}, {"year": 2019, "start_row": 6}],
    "gen_and_fuel": [{"year": 2020, "start_row": 6}, {"year": 2019, "start_row": 6}]
}

# from eia generation and fuel data: "Page 7 File Layout"
eia_sectors = [
    {
        "num": 1,
        "desc": "Electric Utility",
        "long_desc": "Traditional regulated electric utilities", 
    },
    {
        "num": 2,
        "desc": "NAICS-22 Non-Cogen",
        "long_desc": "Independent power producers which are not cogenerators", 
    },
    {
        "num": 3,
        "desc": "NAICS-22 Cogen",
        "long_desc": "Independent power producers which are cogenerators, but whose primary business purpose is the sale of electricity to the public", 
    },
    {
        "num": 4,
        "desc": "Commercial NAICS Non-Cogen",
        "long_desc": "Commercial non-cogeneration facilities that produce electric power, are connected to the gird, and can sell power to the public", 
    },
    {
        "num": 5,
        "desc": "Commercial NAICS Cogen",
        "long_desc": "Commercial cogeneration facilities that produce electric power, are connected to the grid, and can sell power to the public", 
    },
    {
        "num": 6,
        "desc": "Industrial NAICS Non-Cogen",
        "long_desc": "Industrial non-cogeneration facilities that produce electric power, are connected to the gird, and can sell power to the public", 
    },
    {
        "num": 7,
        "desc": "Industrial NAICS Cogen",
        "long_desc": "Industrial cogeneration facilities that produce electric power, are connected to the gird, and can sell power to the public", 
    },
]

nyc_counties = ["new york", "kings", "queens", "richmond", "bronx"]