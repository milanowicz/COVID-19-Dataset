# COVID-19 Dataset

## Case numbers Germany from Robert Koch-Institut (RKI) from Germany

Descriptopn of coloumns:

* Bundesland - Germany province state
* date
* confirmed
* deaths

[COVID-19-RKI](https://github.com/Milanowicz/COVID-19-RKI)


## Case numbers from Johns Hopkins University (JHU) for World

* Combined_Key - from City and so on set by JHU
* City - Since 2X.march city is given
* Province_State
* Country_Region
* Last_Update
* Latitude
* Longitude
* Confirmed
* Deaths
* Recovered
* Active

[COVID-19-JHU](https://github.com/CSSEGISandData/COVID-19)


## Case numbers from USA by The COVID Tracking Project

[The COVID Tracking Project](https://covidtracking.com/api/)


## Install Python environment

Create environment and install Python libs for a GNU/Linux operation system:

    $ . env.sh
    $ pip3 install pandas urllib shutil zipfile


## Update Dataset

    $ . update.sh

or manually

    $ python get_data.py
