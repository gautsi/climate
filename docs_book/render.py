# render templates
from climate.eia import analysis as a
from jinja2 import Template
from pygsutils import general as g

data_path = "./data/eia"

gen_fuel = a.GenFuel(loc=data_path)

specs = [
    {
        "filename": "queens",
        "target": "analysis",
        "ext": "md",
        "parameters": {"queen_top_plants": gen_fuel.list_nyc_plants_top_queens},
    }
]

def get_template(filename) -> Template:
    with open(f"./docs_book/templates/{filename}.jinja", "r") as f:
        template_str = f.read()
    return Template(template_str)

for s in specs:
    template = get_template(s["filename"])
    g.make_dir(f"./docs_book/content/{s['target']}")
    with open(f"./docs_book/content/{s['target']}/{s['filename']}.{s['ext']}", "w") as f:
        f.write(template.render(**s["parameters"]))