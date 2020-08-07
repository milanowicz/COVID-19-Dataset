#!/usr/bin/env python
# coding: utf-8

import urllib.request
from clean import jhu

print('\nDownload COVID-19 dataset from Robert-Koch-Institut')
csv_url = 'https://raw.githubusercontent.com/Milanowicz/COVID-19-RKI/master/csv/rki_data.csv'
csv = 'data/rki/time_series_covid19_confirmed_and_death.csv'
urllib.request.urlretrieve(csv_url, csv)
print('Create file ' + csv + '\n')

print('Download COVID-19 Dataset from Johns Hopkins University (JHU)')
jhu.clean_data()
