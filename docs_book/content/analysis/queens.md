# Fossil fuel power plants in Queens

## Objective
Research the fossil fuel plants in Queens, specifically their history and expansion plans.

### To answer
- what are the top power plants in NYC and Queens?
- what types of fuel do they consume, and in what quantities?

## Data sources
### US Energy Information Administration (EIA)
I use the following data sets from US EIA:
- plant level generation data by month [^eia_plant_gen]
  - the time period specifically looked at here is {glue:text}`start_year`-{glue:text}`end_year`
- shapefiles for plant locations [^eia_shapefiles]

## Analysis
All values are for the time period {glue:text}`start_year`-{glue:text}`end_year`.
### NYC power plants
#### Overall generation
Power plants in NYC generated a total of {glue:text}`ttl_nyc_gwh` gigawatt hours (GWh) of electricity in the time period, an average of {glue:text}`avg_nyc_gwh_per_month` GWh per month.

{glue:}`nyc_year_gwh_chart`

#### Generation by borough

Power plants in Queens accounted for {glue:text}`queens_gwh_pcnt` of generation in the time period.

{glue:}`borough_gwh_chart`

#### Top ten NYC power plants

The top ten power plants in NYC by generation accounted for {glue:text}`top_ten_pcnt` of total NYC generation. Of those plants, {glue:text}`top_ten_queens` are in Queens.

{glue:}`nyc_top_plants_table`

#### NYC fuel mix
{glue:text}`nat_gas_nyc_pcnt` of electricity generated in NYC plants was generated from natural gas.

{glue:}`nyc_fuel_table`

#### Queens top plants fuel mix

The {glue:text}`top_ten_queens` top power plants in Queens consumed {glue:text}`nat_gas_queens_pcnt` of the total natural gas consumed by NYC power plants for electricity generation.

{glue:}`queens_fuel_table`

### Queens power plants



## Questions
- does the "boiler fuel" encompass all consumed fuel? Can check against fuel receipts

[^gen_type]: NYS [data](https://data.ny.gov/Energy-Environment/Electric-Generation-By-Fuel-Type-GWh-Beginning-196/h4gs-8qnu) on electric generation by fuel type, 1960-present 
[^eia_plant_gen]: US EIA plant level generation [data](https://www.eia.gov/electricity/data/eia923/)
[^eia_shapefiles]: US EIA [shapefiles](https://www.eia.gov/maps/layer_info-m.php)
[^nypa_all_gen]: NYPA all generating [facilities](https://www.nypa.gov/power/generation/all-generating-facilities)