# Book

Book for this project made with [jupyter book](https://jupyterbook.org/index.html)

## Setup
- following https://jupyterbook.org/start/overview.html
- using ghp-import for publishing:
```sh
pip install ghp-import
ghp-import -n -p -f ./docs_book/_build/html
```

## Templates
- Template documents are in [./templates](./templates)
- run `python ./docs_book/render.py` to render templates
  - the `render.py` script has specs for template rendering (e.g. parameters, target location)
- Note that resulting source files are derivative and subject to being overwritten! Edit templates instead of resulting source files

## To do
- [x] add plant name to gen/fuel data
- [x] get plant location finer than state
  - can get through shapefile
- [x] NYS net generation by sector
- [x] plant map
- [x] fuel mix of power generation
  - [ ] NYS
  - [x] NYC
  - [x] Queens
  - [x] Queens by plant
- [x] for each plant
  - [ ] map (matplotlib basemap)
  - [ ] over time:
    - [ ] fuel mix
    - [ ] fuel quantity consumed by type
    - [x] generation
  - [ ] proportion of Queens plants
- [x] Queens plants as a proportion of NYC plants