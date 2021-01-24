# specifications

eia_file_specs = {
    "generation": [{"year": 2020, "start_row": 5}, {"year": 2019, "start_row": 6}],
    "gen_and_fuel": [
        {"year": 2020, "start_row": 6},
        {"year": 2019, "start_row": 6},
        {"year": 2018, "start_row": 6},
        {"year": 2017, "start_row": 6},
        {"year": 2016, "start_row": 6},
    ],
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

nyc_boroughs = [
    {
        "county": "new york",
        "borough": "Manhattan",
    },
    {
        "county": "kings",
        "borough": "Brooklyn",
    },
    {
        "county": "queens",
        "borough": "Queens",
    },
    {
        "county": "richmond",
        "borough": "Staten Island",
    },
    {
        "county": "bronx",
        "borough": "Bronx",
    },
]

aer_fuel_types = [
    {"code": "SUN", "desc": "Solar PV and thermal", "renew": True},
    {"code": "COL", "desc": "Coal ", "renew": False},
    {"code": "DFO", "desc": "Distillate Petroleum", "renew": False},
    {"code": "GEO", "desc": "Geothermal", "renew": True},
    {"code": "HPS", "desc": "Hydroelectric Pumped Storage", "renew": True},
    {"code": "HYC", "desc": "Hydroelectric Conventional", "renew": True},
    {
        "code": "MLG",
        "desc": "Biogenic Municipal Solid Waste and Landfill Gas",
        "renew": True,
    },
    {"code": "NG", "desc": "Natural Gas", "renew": False},
    {"code": "NUC", "desc": "Nuclear", "renew": False},
    {"code": "OOG", "desc": "Other Gases", "renew": False},
    {"code": "ORW", "desc": "Other Renewables ", "renew": True},
    {"code": "OTH", "desc": "Other (including nonbiogenic MSW)", "renew": False},
    {"code": "PC", "desc": "Petroleum Coke", "renew": False},
    {"code": "RFO", "desc": "Residual Petroleum", "renew": False},
    {"code": "WND", "desc": "Wind", "renew": True},
    {"code": "WOC", "desc": "Waste Coal", "renew": False},
    {"code": "WOO", "desc": "Waste Oil", "renew": False},
    {"code": "WWW", "desc": "Wood and Wood Waste", "renew": True},
]

table_styles = [
    {"props": [("border-collapse", "separate"), ("border-spacing", "20px 0px")]}
]
