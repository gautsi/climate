# Fossil fuel power plants in Queens

## Objective
 Research the fossil fuel plants in Queens, specifically their history and expansion plans.

### To answer
- what are the top power plants in NYC and Queens?
- what types of fuel do they consume, and in what quantities?

## Data sources
### US Energy Information Administration (EIA)
The use the following data sets from US EIA:
- plant level generation data by month [^eia_plant_gen]
  - the time period specifically looked at here is 2019-July 2020
- shapefiles for plant locations [^eia_shapefiles]

## Analysis
All values are for the time period 2019-July 2020.
### NYC power plants
#### Overall generation
Power plants in NYC generated a total of {glue:text}`ttl_nyc_gwh` gigawatt hours (GWh) of electricity in the time period, an average of {glue:text}`avg_nyc_gwh_per_month` GWh per month.

{glue:}`nyc_month_gwh_chart`

#### Generation by borough

Power plants in Queens accounted for {glue:text}`queens_gwh_pcnt` of generation in the time period.

{glue:}`borough_gwh_chart`

#### Top ten NYC power plants

The top ten power plants in NYC by generation accounted for {glue:text}`top_ten_pcnt` of total NYC generation. Of those plants, {glue:text}`top_ten_queens` are in Queens.

{glue:}`nyc_top_plants_table`

##### NYC fuel mix
{glue:text}`nat_gas_nyc_pcnt` of electricity generated in NYC plants was generated from natural gas.

{glue:}`nyc_fuel_table`

##### Queens top plants fuel mix

The {glue:text}`top_ten_queens` top power plants in Queens consumed {glue:text}`nat_gas_queens_pcnt` of the total natural gas consumed by NYC power plants for electricity generation.

{glue:}`queens_fuel_table`

### Queens power plants


#### Astoria Energy, operated by Astoria Energy LLC
##### Generation
Astoria Energy accounted for {glue:text}`queens_top_gwh_pcnt_55375` of total NYC generation. 

{glue:}`queens_top_month_gwh_chart_55375`
##### Fuel mix

Astoria Energy consumed {glue:text}`queens_top_nat_gas_pcnt_55375` of the total natural gas consumed by NYC power plants for electricity generation.

{glue:}`queens_top_fuel_table_55375`



#### Astoria Energy II, operated by Astoria Energy II LLC
##### Generation
Astoria Energy II accounted for {glue:text}`queens_top_gwh_pcnt_57664` of total NYC generation. 

{glue:}`queens_top_month_gwh_chart_57664`
##### Fuel mix

Astoria Energy II consumed {glue:text}`queens_top_nat_gas_pcnt_57664` of the total natural gas consumed by NYC power plants for electricity generation.

{glue:}`queens_top_fuel_table_57664`



#### 500MW CC, operated by New York Power Authority
##### Generation
500MW CC accounted for {glue:text}`queens_top_gwh_pcnt_56196` of total NYC generation. 

{glue:}`queens_top_month_gwh_chart_56196`
##### Fuel mix

500MW CC consumed {glue:text}`queens_top_nat_gas_pcnt_56196` of the total natural gas consumed by NYC power plants for electricity generation.

{glue:}`queens_top_fuel_table_56196`



#### Ravenswood, operated by Helix Ravenswood, LLC
##### Generation
Ravenswood accounted for {glue:text}`queens_top_gwh_pcnt_2500` of total NYC generation. 

{glue:}`queens_top_month_gwh_chart_2500`
##### Fuel mix

Ravenswood consumed {glue:text}`queens_top_nat_gas_pcnt_2500` of the total natural gas consumed by NYC power plants for electricity generation.

{glue:}`queens_top_fuel_table_2500`



#### Astoria Generating Station, operated by U S Power Generating Company LLC
##### Generation
Astoria Generating Station accounted for {glue:text}`queens_top_gwh_pcnt_8906` of total NYC generation. 

{glue:}`queens_top_month_gwh_chart_8906`
##### Fuel mix

Astoria Generating Station consumed {glue:text}`queens_top_nat_gas_pcnt_8906` of the total natural gas consumed by NYC power plants for electricity generation.

{glue:}`queens_top_fuel_table_8906`



#### Kennedy International Airport Cogen, operated by KIAC Partners
##### Generation
Kennedy International Airport Cogen accounted for {glue:text}`queens_top_gwh_pcnt_54114` of total NYC generation. 

{glue:}`queens_top_month_gwh_chart_54114`
##### Fuel mix

Kennedy International Airport Cogen consumed {glue:text}`queens_top_nat_gas_pcnt_54114` of the total natural gas consumed by NYC power plants for electricity generation.

{glue:}`queens_top_fuel_table_54114`




## Questions
- does the "boiler fuel" encompass all consumed fuel? Can check against fuel receipts

## To do
- [x] add plant name to gen/fuel data
- [x] get plant location finer than state
  - can get through shapefile
- [x] NYS net generation by sector
- [x] plant map
- [ ] fuel mix of power generation
  - [ ] NYS
  - [ ] NYC
  - [ ] Queens
  - [ ] Queens by plant
- [ ] for each plant
  - [ ] map (matplotlib basemap)
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