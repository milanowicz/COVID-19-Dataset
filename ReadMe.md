# COVID-19 Dataset

## Case numbers Germany from Robert Koch-Institut (RKI) from Germany

Description of columns:

* State - Bundesland
* Update
* Confirmed
* Deaths

[COVID-19-RKI](https://github.com/Milanowicz/COVID-19-RKI)


## Case numbers from Johns Hopkins University (JHU) for World

Description of columns:

* City - Since 2X.march city is given
* State
* Country
* Update
* Latitude
* Longitude
* Confirmed
* Deaths
* Recovered

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
