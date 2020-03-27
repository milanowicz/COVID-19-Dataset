# COVID-19 Dataset

This COVID-19 Dataset should be used for Data Sciene.
Therefore the columns are the same for JHU and RKI data to load them with pandas.


## Case numbers Germany from Robert Koch-Institut (RKI) in Germany

Description of columns:

<table>
<tr>
<th>State</th><th>Update</th><th>Confirmed</th><th>Deaths</th>
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

Description of columns:

<table>
<tr>
<th>City</th><th>State</th><th>Country</th><th>Update</th><th>Latitude</th><th>Longitude</th><th>Confirmed</th><th>Deaths</th><th>Recovered</th>
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
</tr>
</table>

[COVID-19-JHU](https://github.com/CSSEGISandData/COVID-19)


## Case numbers from USA collecting by The COVID Tracking Project

Future use to analyze it.....

[The COVID Tracking Project](https://covidtracking.com/api/)


## Install Python environment

Create environment and install Python libs for a GNU/Linux operation system:

    $ . env.sh
    $ pip3 install pandas urllib shutil zipfile


## Update Dataset

    $ . update.sh

or manually

    $ python get_data.py
