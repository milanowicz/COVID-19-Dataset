#!/usr/bin/env python
# coding: utf-8

import urllib.request
import os
import shutil
import zipfile

csv_url = 'https://raw.githubusercontent.com/Milanowicz/COVID-19-RKI/master/csv/rki_data.csv'
urllib.request.urlretrieve(csv_url, 'data/rki/time_series_confirmed_and_death.csv')


csv_url = 'https://github.com/CSSEGISandData/COVID-19/archive/master.zip'
zip = 'data/jhu/data.zip'
urllib.request.urlretrieve(csv_url, zip)
with zipfile.ZipFile(zip, 'r') as zip_ref:
    zip_ref.extractall('data/jhu/data')
os.remove(zip)

shutil.rmtree('data/jhu/data')
