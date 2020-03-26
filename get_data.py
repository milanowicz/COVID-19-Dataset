#!/usr/bin/env python
# coding: utf-8

import urllib.request
import os
import pandas as pd
import shutil
import zipfile

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

# Collecting data from Johns Hopkins University and create a big data frame
# CSV files have different columns, this is the task here
df_data = pd.DataFrame()
unknown_columns = []
columns = [
    'Province/State,Country/Region,Last Update,Confirmed,Deaths,Recovered',
    'Province/State,Country/Region,Last Update,Confirmed,Deaths,Recovered,Latitude,Longitude',
    'FIPS,Admin2,Province_State,Country_Region,Last_Update,Lat,Long_,Confirmed,Deaths,Recovered,Active,Combined_Key'
]
df_1 = pd.DataFrame(columns=columns[0].split(','))
df_2 = pd.DataFrame(columns=columns[1].split(','))
df_3 = pd.DataFrame(columns=columns[2].split(','))
print('Parse CSV files from JHU into a Pandas DataFrame')
for dirname, _, filenames in os.walk('data/jhu/data/COVID-19-master/csse_covid_19_data/csse_covid_19_daily_reports'):
    for filename in filenames:
        if filename != '.gitignore' and filename != 'README.md':
            file = os.path.join(dirname, filename)
            with open(file) as f:
                line = f.readline().strip()
                line = line.replace(u'\ufeff', '')
                if line not in columns and line not in unknown_columns:
                    unknown_columns.append(line)
            df_0 = pd.read_csv(file, parse_dates=True)
            try:
                df_0['Last_Update'] = pd.to_datetime(df_0['Last_Update'].astype(str), format='%m/%d/%Y %H:%M')
                df_0['Last_Update'] = df_0['Last_Update'].astype(object).where(df_0['Last_Update'].notnull(), None)
            except KeyError:
                try:
                    df_0['Last Update'] = pd.to_datetime(df_0['Last Update'].astype(str), format='%m/%d/%Y %H:%M')
                    df_0['Last Update'] = df_0['Last Update'].astype(object).where(df_0['Last Update'].notnull(), None)
                except ValueError:
                    try:
                        df_0['Last Update'] = pd.to_datetime(df_0['Last Update'].astype(str), format='%m/%d/%y %H:%M')
                        df_0['Last Update'] = df_0['Last Update'].astype(object).where(df_0['Last Update'].notnull(), None)
                    except ValueError:
                        df_0['Last Update'] = pd.to_datetime(df_0['Last Update'].astype(str), format='%Y-%m-%d %H:%M')
                        df_0['Last Update'] = df_0['Last Update'].astype(object).where(df_0['Last Update'].notnull(), None)
            except ValueError:
                try:
                    df_0['Last_Update'] = pd.to_datetime(df_0['Last_Update'].astype(str), format='%m/%d/%y %H:%M')
                    df_0['Last_Update'] = df_0['Last_Update'].astype(object).where(df_0['Last_Update'].notnull(), None)
                except ValueError:
                    df_0['Last_Update'] = pd.to_datetime(df_0['Last_Update'].astype(str), format='%Y-%m-%d %H:%M')
                    df_0['Last_Update'] = df_0['Last_Update'].astype(object).where(df_0['Last_Update'].notnull(), None)
            if line == columns[0]:
                df_1 = pd.concat([df_1, df_0])
            elif line == columns[1]:
                df_2 = pd.concat([df_2, df_0])
            elif line == columns[2]:
                df_3 = pd.concat([df_3, df_0])

# Detect if one new column has come up
if len(unknown_columns) > 0:
    print('Found COLUMNS are unknown!\n')
    for line in unknown_columns:
        print('\t' + line)
    print('')


# Clean data sources to merge them in one dataframe
df_1['Confirmed'].fillna(0, inplace=True)
df_1['Deaths'].fillna(0, inplace=True)
df_1['Recovered'].fillna(0, inplace=True)
df_1['Province_State'] = df_1['Province/State']
del df_1['Province/State']
df_1['Country_Region'] = df_1['Country/Region']
del df_1['Country/Region']
df_1['Last_Update'] = df_1['Last Update']
del df_1['Last Update']

df_2['Confirmed'].fillna(0, inplace=True)
df_2['Deaths'].fillna(0, inplace=True)
df_2['Recovered'].fillna(0, inplace=True)
df_2['Province_State'] = df_2['Province/State']
del df_2['Province/State']
df_2['Country_Region'] = df_2['Country/Region']
del df_2['Country/Region']
df_2['Last_Update'] = df_2['Last Update']
del df_2['Last Update']

df_3['Confirmed'].fillna(0, inplace=True)
df_3['Deaths'].fillna(0, inplace=True)
df_3['Recovered'].fillna(0, inplace=True)
df_3['Latitude'] = df_3['Lat']
del df_3['Lat']
df_3['Longitude'] = df_3['Long_']
del df_3['Long_']
del df_3['FIPS']
df_3['City'] = df_3['Admin2']
del df_3['Admin2']


# Merge Dataframes into one Big to write it to a CSV file
columns = ['Combined_Key', 'City', 'Province_State', 'Country_Region', 'Last_Update',
           'Latitude', 'Longitude', 'Confirmed', 'Deaths', 'Recovered',
           'Active']
frames = [df_1, df_2, df_3]
df = pd.DataFrame(pd.concat(frames), columns=columns)
df.reset_index(inplace=True, drop=True)
df['City'].fillna('', inplace=True)
df['Province_State'].fillna('', inplace=True)
df['Combined_Key'].fillna('', inplace=True)
csv = 'data/jhu/time_series_confirmed_deaths_recovered.csv'
df.to_csv(csv)
print('Create file ' + csv + '\n')

shutil.rmtree('data/jhu/data')
