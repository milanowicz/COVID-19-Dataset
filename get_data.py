#!/usr/bin/env python
# coding: utf-8

import urllib.request
import os
import shutil
import zipfile
from clean import jhu

print('\nDownload COVID-19 dataset from Robert-Koch-Institut')
csv_url = 'https://raw.githubusercontent.com/Milanowicz/COVID-19-RKI/master/csv/rki_data.csv'
csv = 'data/rki/time_series_confirmed_and_death.csv'
urllib.request.urlretrieve(csv_url, csv)
print('Create file ' + csv + '\n')

print('Download COVID-19 daily dataset from The COVID Tracking Project')
csv_url = 'https://covidtracking.com/api/us/daily.csv'
csv = 'data/us/time_series_us_daily.csv'
urllib.request.urlretrieve(csv_url, csv)
print('Create file ' + csv + '\n')

print('Download COVID-19 states daily dataset from The COVID Tracking Project')
csv_url = 'http://covidtracking.com/api/states/daily.csv'
csv = 'data/us/time_series_states_daily.csv'
urllib.request.urlretrieve(csv_url, csv)
print('Create file ' + csv + '\n')

# csv_url = 'https://raw.githubusercontent.com/beoutbreakprepared/nCoV2019/master/latest_data/latestdata.csv'
# csv = 'data/COVID19_2020_open_line_list.csv'
# urllib.request.urlretrieve(csv_url, csv)
# print('Create file ' + csv)

print('Download COVID-19 Dataset from Johns Hopkins University (JHU)')
csv_url = 'https://github.com/CSSEGISandData/COVID-19/archive/master.zip'
zip = 'data/jhu/data.zip'
urllib.request.urlretrieve(csv_url, zip)
with zipfile.ZipFile(zip, 'r') as zip_ref:
    zip_ref.extractall('data/jhu/data')
os.remove(zip)

jhu.get_data()

shutil.rmtree('data/jhu/data')
