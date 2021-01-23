# New York State generated electricity fuel mix

## Objective
See which fuels are most used to generated electricity in New York State, and how that has changed over time

## Yearly fuel mix
### Average GW
{glue:}`fm_yr_chrt`
### Percent of total
The proportion of NYS electricity generation from nuclear clealy dips from 2019 to 2020, and coincides with a equivalent increase in the proportion of generation from fossil fuels. 
{glue:}`fm_yr_pcnt_chrt`

## Monthly fuel mix
### Average GW
As a stacked bar chart:
{glue:}`fm_mo_chrt`

As a line chart, shows again the dip in nuclear, can now place in early 2020. Unclear from this chart what replaces it.
{glue:}`fm_mo_line_chrt`

#### Rolling 12-month average

As a rolling 12-month average, although renewables show a steady but slow increase, dip in nuclear seems replaced by fossil fuels.

{glue:}`fm_mo_rolling_chrt`

### Percent of total
{glue:}`fm_mo_pcnt_chrt`

#### Rolling 12-month average

The replacement of nuclear with fossil fuels is most evident in the rolling 12-month average of proportions.

{glue:}`fm_mo_rolling_pcnt_chrt`


## Data sources
### New York Independent System Operator (NYISO)
I use the following data set from NYISO:
- fuel mix for NYS electricity generation every 5 minutes [^nyiso_fuel_mix]
  - the time period specifically looked at here is {glue:text}`nyiso_start_year`-{glue:text}`nyiso_end_year`



[^nyiso_fuel_mix]: csvs here: [http://mis.nyiso.com/public/P-63list.htm](http://mis.nyiso.com/public/P-63list.htm), also see the real-time dashboard here: [https://www.nyiso.com/real-time-dashboard](https://www.nyiso.com/real-time-dashboard)