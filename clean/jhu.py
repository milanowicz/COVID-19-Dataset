import os
import pandas as pd
import shutil
import wget

class jhu:
    @staticmethod
    def clean_data():
        path = 'data/jhu/data/'
        try:
            os.mkdir(path)
        except OSError:
            shutil.rmtree(path)
        urls = [
            'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
            'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv',
            'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'
        ]

        for url in urls:
            filename = wget.download(url, path)
        conf_df = pd.read_csv(path + 'time_series_covid19_confirmed_global.csv')
        deaths_df = pd.read_csv(path + 'time_series_covid19_deaths_global.csv')
        recv_df = pd.read_csv(path + 'time_series_covid19_recovered_global.csv')

        dates = conf_df.columns[4:]
        conf_df_long = conf_df.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                                    value_vars=dates, var_name='Date', value_name='Confirmed')

        deaths_df_long = deaths_df.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                                        value_vars=dates, var_name='Date', value_name='Deaths')

        recv_df_long = recv_df.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                                    value_vars=dates, var_name='Date', value_name='Recovered')

        full_table = pd.concat([conf_df_long, deaths_df_long['Deaths'], recv_df_long['Recovered']], axis=1, sort=False)
        full_table = full_table[full_table['Province/State'].str.contains(',') != True]

        # Rename columns
        full_table['Country/Region'] = full_table['Country/Region'].replace('Korea, South', 'South Korea')
        full_table.rename(columns={'Country/Region': 'Country', 'Province/State': 'State'}, inplace=True)
        full_table.rename(columns={'Lat': 'Latitude', 'Long': 'Longitude'}, inplace=True)

        # replacing Mainland china with just China
        full_table['Country'] = full_table['Country'].replace('Mainland China', 'China')
        # Active Case = confirmed - deaths - recovered
        full_table['Active'] = full_table['Confirmed'] - full_table['Deaths'] - full_table['Recovered']
        # Fill all numbers with zeros
        cases = ['Confirmed', 'Deaths', 'Recovered', 'Active']
        full_table[cases] = full_table[cases].fillna(0)

        csv = 'data/jhu/time_series_covid19_confirmed_deaths_recovered.csv'
        full_table.to_csv(csv, index=False)
        shutil.rmtree(path)
        print('Create file ' + csv + '\n')
