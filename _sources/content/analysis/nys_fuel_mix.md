# New York State generated electricity fuel mix

## Objective
See which fuels are most used to generated electricity in New York State, and how that has changed over time

## Yearly fuel mix
### Total GWh
{glue:}`fm_yr_chrt`
### Percent of total
{glue:}`fm_yr_pcnt_chrt`

## Monthly fuel mix
### Total Gwh
{glue:}`fm_mo_chrt`
### Percent of total
{glue:}`fm_mo_pcnt_chrt`


## Data sources
### New York Independent System Operator (NYISO)
I use the following data set from NYISO:
- fuel mix for NYS electricity generation every 5 minutes [^nyiso_fuel_mix]
  - the time period specifically looked at here is {glue:text}`nyiso_start_year`-{glue:text}`nyiso_end_year`



[^nyiso_fuel_mix]: csvs here: [http://mis.nyiso.com/public/P-63list.htm](http://mis.nyiso.com/public/P-63list.htm), also see the real-time dashboard here: [https://www.nyiso.com/real-time-dashboard](https://www.nyiso.com/real-time-dashboard)