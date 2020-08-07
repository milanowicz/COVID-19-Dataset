# COVID-19 Dataset

This COVID-19 Dataset should be used for Data Sciene.
Therefore the columns are the same for JHU and RKI data to load them with pandas.


## Case numbers Germany from Robert Koch-Institut (RKI) in Germany

Description of columns:

<table>
<tr>
<th>State</th><th>Date</th><th>Confirmed</th><th>Deaths</th>
</tr>
<tr>
<td>Name of federal state (German Bundesland)</td>
<td>Date in %Y-%m-%d format</td>
<td>Numbers of confirmed cases</td>
<td>Numbers of deaths</td>
</tr>
</table>

[COVID-19-RKI](https://github.com/Milanowicz/COVID-19-RKI)


## Case numbers from Johns Hopkins University (JHU) for the World

[COVID-19-JHU](https://github.com/CSSEGISandData/COVID-19)


### Data by day

Description of columns:

    Data: data/jhu/time_series_covid19_confirmed_deaths_recovered.csv

<table>
<tr>
<th>City</th><th>State</th><th>Country</th><th>Date</th><th>Latitude</th><th>Longitude</th><th>Confirmed</th><th>Deaths</th><th>Recovered</th><th>Active</th><th>WHO Region</th>
</tr>
<tr>
<td>Name from City</td>
<td>Name of federal state</td>
<td>Name from Country</td>
<td>Date in %Y-%m-%d format</td>
<td>Latitude</td>
<td>Longitude</td>
<td>Numbers of confirmed cases</td>
<td>Numbers of deaths</td>
<td>Numbers of recovered</td>
<td>Active = Confirmed - Deaths - Recovered</td>
<td>WHO Region</td>
</tr>
</table>


### Grouped by Day and Country

    Data: data/jhu/time_series_covid19_grouped_day_country.csv

<table>
<tr>
<th>Date</th><th>Country</th><th>Confirmed</th><th>Deaths</th><th>Recovered</th><th>Active</th><th>New cases</th><th>New deaths</th><th>New recovered</th><th>WHO Region</th>
</tr>
<tr>
<td>Date in %Y-%m-%d format</td>
<td>Name from Country</td>
<td>Numbers of confirmed cases</td>
<td>Numbers of deaths</td>
<td>Numbers of recovered</td>
<td>Active = Confirmed - Deaths - Recovered</td>
<td>New cases / Day</td>
<td>New deaths / Day</td>
<td>New recovered / Day</td>
<td>WHO Region</td>
</tr>
</table>

### Grouped by all Countries together

    Data: data/jhu/time_series_covid19_grouped_by_countries.csv
    
    Columns:

        Country
        Confirmed
        Deaths
        Recovered
        Active
        New cases
        New deaths
        New recovered
        Deaths / 100 Cases
        Recovered / 100 Cases
        Deaths / 100 Recovered
        Confirmed last week
        1 week change
        1 week % increase
        WHO Region

### Grouped by all Days together

    Data: data/jhu/time_series_covid19_grouped_by_days.csv

    Columns:

        Date
        Confirmed
        Deaths
        Recovered
        Active
        New cases
        New deaths
        New recovered
        Deaths / 100 Cases
        Recovered / 100 Cases
        Deaths / 100 Recovered
        Country Number


## Common data description

Population CSV files

The dataset contains population data of different countries/regions from 1960 to 2018.
There are condensed and region-wise data in the population dataset.

Origin: https://data.worldbank.org/indicator/SP.POP.TOTL

[Kaggle Competion](https://www.kaggle.com/imdevskp/world-population-19602018)


## Install Python environment

Create environment and install Python libs for a GNU/Linux operation system:

    $ . env.sh
    $ pip3 install pandas urllib shutil wget


## Update Dataset

Update data only

    $ . update.sh

Update, commit and push data 

    $ . aupdate.sh

or manually

    $ python get_data.py
