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
            os.mkdir(path)
        urls = [
            'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
            'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv',
            'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'
        ]

        # Download Datasets
        for url in urls:
            filename = wget.download(url, path)
        # Read all csv files intro Pandas DataFrame
        conf_df = pd.read_csv(path + 'time_series_covid19_confirmed_global.csv')
        deaths_df = pd.read_csv(path + 'time_series_covid19_deaths_global.csv')
        recv_df = pd.read_csv(path + 'time_series_covid19_recovered_global.csv')

        # Get all dates by columns
        dates = conf_df.columns[4:]
        # Merging DataFrames
        conf_df_long = conf_df.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                                    value_vars=dates, var_name='Date', value_name='Confirmed')

        deaths_df_long = deaths_df.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                                        value_vars=dates, var_name='Date', value_name='Deaths')

        recv_df_long = recv_df.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'],
                                    value_vars=dates, var_name='Date', value_name='Recovered')

        full_table = pd.merge(left=conf_df_long, right=deaths_df_long, how='left',
                              on=['Province/State', 'Country/Region', 'Date', 'Lat', 'Long'])
        full_table = pd.merge(left=full_table, right=recv_df_long, how='left',
                              on=['Province/State', 'Country/Region', 'Date', 'Lat', 'Long'])

        # Denmark Islands
        full_table['Country/Region'].mask(full_table['Province/State'] == 'Faroe Islands', 'Faroe Islands (DK)', inplace=True)
        full_table['Country/Region'].mask(full_table['Province/State'] == 'Greenland', 'Greenland (DK)', inplace=True)
        # French Islands
        full_table['Country/Region'].mask(full_table['Province/State'] == 'French Guiana', 'French Guiana', inplace=True)
        full_table['Country/Region'].mask(full_table['Province/State'] == 'French Polynesia', 'French Polynesia', inplace=True)
        full_table['Country/Region'].mask(full_table['Province/State'] == 'Guadeloupe', 'Guadeloupe (FR)', inplace=True)
        full_table['Country/Region'].mask(full_table['Province/State'] == 'Mayotte', 'Mayotte (FR)', inplace=True)
        full_table['Country/Region'].mask(full_table['Province/State'] == 'Reunion', 'Reunion (FR)', inplace=True)
        full_table['Country/Region'].mask(full_table['Province/State'] == 'Martinique', 'Martinique (FR)', inplace=True)
        full_table['Country/Region'].mask(full_table['Province/State'] == 'Saint Pierre and Miquelon', 'Saint Pierre and Miquelon (FR)', inplace=True)
        # Netherlands Islands
        full_table['Country/Region'].mask(full_table['Province/State'] == 'Aruba', 'Aruba (NL)', inplace=True)
        full_table['Country/Region'].mask(full_table['Province/State'] == 'Curacao', 'Curacao (NL)', inplace=True)
        full_table['Country/Region'].mask(full_table['Province/State'] == 'Sint Maarten', 'Sint Maarten (NL)', inplace=True)
        full_table['Country/Region'].mask(full_table['Province/State'] == 'Bonaire, Sint Eustatius and Saba', 'Bonaire, Sint Eustatius and Saba (NL)', inplace=True)
        # U.K. Islands
        full_table['Country/Region'].mask(full_table['Province/State'] == 'Cayman Islands', 'Cayman Islands (UK)', inplace=True)
        full_table['Country/Region'].mask(full_table['Province/State'] == 'Gibraltar', 'Gibraltar (UK)', inplace=True)
        full_table['Country/Region'].mask(full_table['Province/State'] == 'Montserrat', 'Montserrat (UK)', inplace=True)
        full_table['Country/Region'].mask(full_table['Province/State'] == 'Anguilla', 'Anguilla (UK)', inplace=True)
        full_table['Country/Region'].mask(full_table['Province/State'] == 'Turks and Caicos Islands', 'Turks and Caicos Islands (UK)', inplace=True)
        full_table['Country/Region'].mask(full_table['Province/State'] == 'British Virgin Islands', 'British Virgin Islands (UK)', inplace=True)
        full_table['Country/Region'].mask(full_table['Province/State'] == 'Falkland Islands (Malvinas)', 'Falkland Islands (Malvinas) (UK)', inplace=True)

        full_table[full_table['Recovered'].isna()]['Country/Region'].value_counts()
        full_table[full_table['Recovered'].isna()]['Date'].value_counts()
        full_table['Recovered'] = full_table['Recovered'].fillna(0)
        full_table['Recovered'] = full_table['Recovered'].astype('int')

        # full_table = pd.concat([conf_df_long, deaths_df_long['Deaths'], recv_df_long['Recovered']], axis=1, sort=False)
        full_table = full_table[full_table['Province/State'].str.contains(',') != True]

        # Fixing off data from WHO data
        feb_12_conf = {'Hubei': 34874}

        # function to change value
        def change_val(date, ref_col, val_col, dtnry):
            for key, val in dtnry.items():
                full_table.loc[(full_table['Date'] == date) & (full_table[ref_col] == key), val_col] = val
        # changing values
        change_val('2/12/20', 'Province/State', 'Confirmed', feb_12_conf)

        # Rename columns
        full_table.rename(columns={'Country/Region': 'Country', 'Province/State': 'State'}, inplace=True)
        full_table.rename(columns={'Lat': 'Latitude', 'Long': 'Longitude'}, inplace=True)

        # Changing Korea, South to South Korea
        full_table['Country'] = full_table['Country'].replace('Korea, South', 'South Korea')
        # Replacing Mainland china with just China
        full_table['Country'] = full_table['Country'].replace('Mainland China', 'China')
        # Clean case columns to zero when is na
        cases = ['Confirmed', 'Deaths', 'Recovered']
        full_table[cases] = full_table[cases].fillna(0)
        # Active Case = confirmed - deaths - recovered
        full_table['Active'] = full_table['Confirmed'] - full_table['Deaths'] - full_table['Recovered']
        # Fill all numbers with zeros
        cases = ['Confirmed', 'Deaths', 'Recovered', 'Active']
        full_table[cases] = full_table[cases].fillna(0)

        csv = 'data/jhu/time_series_covid19_confirmed_deaths_recovered.csv'
        full_table.to_csv(csv, index=False)
        shutil.rmtree(path)
        print('Create file ' + csv + '\n')
