# Fossil fuel power plants in Queens

## Objective
 Research the fossil fuel plants in Queens, specifically their history and expansion plans.

### To answer
- which power plants are in Queens?
- what types of fuel do they recieve, and in what quantities?

## Data sources
### US Energy Information Administration (EIA)
- plant level generation data by month [^eia_plant_gen]
- shapefiles for plant locations [^eia_shapefiles]

## Questions
- does the "boiler fuel" encompass all consumed fuel? Can check against fuel receipts

## To do
- [x] add plant name to gen/fuel data
- [x] get plant location finer than state
  - can get through shapefile
- [ ] NYS net generation by sector
- [ ] plant map
- [ ] for each plant
  - [ ] over time:
    - [ ] fuel mix
    - [ ] fuel quantity consumed by type
    - [ ] generation
  - [ ] proportion of Queens plants
- [ ] Queens plants as a proportion of NYC plants

[^gen_type]: NYS [data](https://data.ny.gov/Energy-Environment/Electric-Generation-By-Fuel-Type-GWh-Beginning-196/h4gs-8qnu) on electric generation by fuel type, 1960-present 
[^eia_plant_gen]: US EIA plant level generation [data](https://www.eia.gov/electricity/data/eia923/)
[^eia_shapefiles]: US EIA [shapefiles](https://www.eia.gov/maps/layer_info-m.php)
[^nypa_all_gen]: NYPA all generating [facilities](https://www.nypa.gov/power/generation/all-generating-facilities)
