import os
import numpy as np
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
        full_table['Country/Region'].mask(full_table['Province/State'] == 'Faroe Islands', 'Faroe Islands (DK)',
                                          inplace=True)
        full_table['Country/Region'].mask(full_table['Province/State'] == 'Greenland', 'Greenland (DK)', inplace=True)
        # French Islands
        full_table['Country/Region'].mask(full_table['Province/State'] == 'French Guiana', 'French Guiana',
                                          inplace=True)
        full_table['Country/Region'].mask(full_table['Province/State'] == 'French Polynesia', 'French Polynesia',
                                          inplace=True)
        full_table['Country/Region'].mask(full_table['Province/State'] == 'Guadeloupe', 'Guadeloupe (FR)', inplace=True)
        full_table['Country/Region'].mask(full_table['Province/State'] == 'Mayotte', 'Mayotte (FR)', inplace=True)
        full_table['Country/Region'].mask(full_table['Province/State'] == 'Reunion', 'Reunion (FR)', inplace=True)
        full_table['Country/Region'].mask(full_table['Province/State'] == 'Martinique', 'Martinique (FR)', inplace=True)
        full_table['Country/Region'].mask(full_table['Province/State'] == 'Saint Pierre and Miquelon',
                                          'Saint Pierre and Miquelon (FR)', inplace=True)
        # Netherlands Islands
        full_table['Country/Region'].mask(full_table['Province/State'] == 'Aruba', 'Aruba (NL)', inplace=True)
        full_table['Country/Region'].mask(full_table['Province/State'] == 'Curacao', 'Curacao (NL)', inplace=True)
        full_table['Country/Region'].mask(full_table['Province/State'] == 'Sint Maarten', 'Sint Maarten (NL)',
                                          inplace=True)
        full_table['Country/Region'].mask(full_table['Province/State'] == 'Bonaire, Sint Eustatius and Saba',
                                          'Bonaire, Sint Eustatius and Saba (NL)', inplace=True)
        # U.K. Islands
        full_table['Country/Region'].mask(full_table['Province/State'] == 'Cayman Islands', 'Cayman Islands (UK)',
                                          inplace=True)
        full_table['Country/Region'].mask(full_table['Province/State'] == 'Gibraltar', 'Gibraltar (UK)', inplace=True)
        full_table['Country/Region'].mask(full_table['Province/State'] == 'Montserrat', 'Montserrat (UK)', inplace=True)
        full_table['Country/Region'].mask(full_table['Province/State'] == 'Anguilla', 'Anguilla (UK)', inplace=True)
        full_table['Country/Region'].mask(full_table['Province/State'] == 'Turks and Caicos Islands',
                                          'Turks and Caicos Islands (UK)', inplace=True)
        full_table['Country/Region'].mask(full_table['Province/State'] == 'British Virgin Islands',
                                          'British Virgin Islands (UK)', inplace=True)
        full_table['Country/Region'].mask(full_table['Province/State'] == 'Falkland Islands (Malvinas)',
                                          'Falkland Islands (Malvinas) (UK)', inplace=True)

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

        # ship rows containing ships with COVID-19 reported cases
        ship_rows = full_table['State'].str.contains('Grand Princess') | \
                    full_table['State'].str.contains('Diamond Princess') | \
                    full_table['Country'].str.contains('Diamond Princess') | \
                    full_table['Country'].str.contains('MS Zaandam')

        # skipping rows with ships info
        full_table = full_table[~(ship_rows)]

        full_table['WHO Region'] = full_table['Country'].map(jhu.get_who_regions())

        # find missing values
        print(full_table[full_table['WHO Region'].isna()]['Country'].unique())

        csv = 'data/jhu/time_series_covid19_confirmed_deaths_recovered.csv'
        full_table.to_csv(csv, index=False)
        shutil.rmtree(path)
        print('Create file ' + csv + '\n')

        # Grouped by day, country
        full_grouped = full_table.groupby(['Date', 'Country'])['Confirmed', 'Deaths', 'Recovered', 'Active'] \
            .sum().reset_index()

        # new cases ======================================================
        temp = full_grouped.groupby(['Country', 'Date', ])['Confirmed', 'Deaths', 'Recovered']
        temp = temp.sum().diff().reset_index()

        mask = temp['Country'] != temp['Country'].shift(1)

        temp.loc[mask, 'Confirmed'] = np.nan
        temp.loc[mask, 'Deaths'] = np.nan
        temp.loc[mask, 'Recovered'] = np.nan

        # renaming columns
        temp.columns = ['Country', 'Date', 'New cases', 'New deaths', 'New recovered']
        # =================================================================

        # merging new values
        full_grouped = pd.merge(full_grouped, temp, on=['Country', 'Date'])

        # filling na with 0
        full_grouped = full_grouped.fillna(0)

        # fixing data types
        cols = ['New cases', 'New deaths', 'New recovered']
        full_grouped[cols] = full_grouped[cols].astype('int')

        full_grouped['New cases'] = full_grouped['New cases'].apply(lambda x: 0 if x < 0 else x)
        full_grouped['WHO Region'] = full_grouped['Country'].map(jhu.get_who_regions())
        csv = 'data/jhu/time_series_covid19_grouped_day_country.csv'
        full_grouped.to_csv(csv, index=False)

    @staticmethod
    def get_who_regions():
        who_region = {}

        # African Region AFRO
        afro = "Algeria, Angola, Cabo Verde, Eswatini, Sao Tome and Principe, Benin, South Sudan, Western Sahara, " \
               "Congo (Brazzaville), Congo (Kinshasa), Cote d'Ivoire, Botswana, Burkina Faso, Burundi, Cameroon, " \
               "Cape Verde, Central African Republic, Chad, Comoros, Ivory Coast, Democratic Republic of the Congo, " \
               "Equatorial Guinea, Eritrea, Ethiopia, Gabon, Gambia, Ghana, Guinea, Guinea-Bissau, Kenya, Lesotho, " \
               "Liberia, Madagascar, Malawi, Mali, Mauritania, Mauritius, Mozambique, Namibia, Niger, Nigeria, " \
               "Republic of the Congo, Rwanda, São Tomé and Príncipe, Senegal, Seychelles, Sierra Leone, Somalia, " \
               "South Africa, Swaziland, Togo, Uganda, Tanzania, Zambia, Zimbabwe, Mayotte (FR), Reunion (FR), " \
               "Falkland Islands (Malvinas) (UK) "
        afro = [i.strip() for i in afro.split(',')]
        for i in afro:
            who_region[i] = 'Africa'

        # Region of the Americas PAHO
        paho = 'Antigua and Barbuda, Argentina, Bahamas, Barbados, Belize, Bolivia, Brazil, Canada, Chile, Colombia, ' \
               'Costa Rica, Cuba, Dominica, Dominican Republic, Ecuador, El Salvador, Grenada, Guatemala, Guyana, ' \
               'Haiti, Honduras, Jamaica, Mexico, Nicaragua, Panama, Paraguay, Peru, Saint Kitts and Nevis, ' \
               'Saint Lucia, Saint Vincent and the Grenadines, Suriname, Trinidad and Tobago, United States, US, ' \
               'Uruguay, Venezuela, Martinique (FR), Aruba (NL), Curacao (NL), Sint Maarten (NL), Cayman Islands (' \
               'UK), Montserrat (UK), Anguilla (UK), British Virgin Islands (UK), Turks and Caicos Islands (UK), ' \
               'Saint Pierre and Miquelon (FR), Guadeloupe (FR), French Guiana '
        paho = [i.strip() for i in paho.split(',')]
        for i in paho:
            who_region[i] = 'Americas'

        # South-East Asia Region SEARO
        searo = 'Bangladesh, Bhutan, North Korea, India, Indonesia, Maldives, Myanmar, Burma, Nepal, Sri Lanka, ' \
                'Thailand, Timor-Leste '
        searo = [i.strip() for i in searo.split(',')]
        for i in searo:
            who_region[i] = 'South-East Asia'

        # European Region EURO
        euro = 'Albania, Andorra, Greenland (DK), Kosovo, Holy See, Liechtenstein, Armenia, Czechia, Austria, ' \
               'Azerbaijan, Belarus, Belgium, Bosnia and Herzegovina, Bulgaria, Croatia, Cyprus, Czech Republic, ' \
               'Denmark, ' \
               'Estonia, Finland, France, Georgia, Germany, Greece, Hungary, Iceland, Ireland, Israel, Italy, ' \
               'Kazakhstan, Kyrgyzstan, Latvia, Lithuania, Luxembourg, Malta, Monaco, Montenegro, Netherlands, ' \
               'North Macedonia, Norway, Poland, Portugal, Moldova, Romania, Russia, San Marino, Serbia, Slovakia, ' \
               'Slovenia, Spain, Sweden, Switzerland, Tajikistan, Turkey, Turkmenistan, Ukraine, United Kingdom, ' \
               'Uzbekistan, Gibraltar (UK) '
        euro = [i.strip() for i in euro.split(',')]
        for i in euro:
            who_region[i] = 'Europe'

        # Eastern Mediterranean Region EMRO
        emro = 'Afghanistan, Bahrain, Djibouti, Egypt, Iran, Iraq, Jordan, Kuwait, Lebanon, Libya, Morocco, Oman, ' \
               'Pakistan, Palestine, West Bank and Gaza, Qatar, Saudi Arabia, Somalia, Sudan, Syria, Tunisia, ' \
               'United Arab Emirates, Yemen '
        emro = [i.strip() for i in emro.split(',')]
        for i in emro:
            who_region[i] = 'Eastern Mediterranean'

        # Western Pacific Region WPRO
        wpro = 'Australia, Brunei, Cambodia, China, Cook Islands, Fiji, Japan, Kiribati, Laos, Malaysia, Marshall ' \
               'Islands, Micronesia, Mongolia, Nauru, New Zealand, Niue, Palau, Papua New Guinea, Philippines, ' \
               'South Korea, Samoa, Singapore, Solomon Islands, Taiwan, Taiwan*, Tonga, Tuvalu, Vanuatu, Vietnam, ' \
               'French Polynesia '
        wpro = [i.strip() for i in wpro.split(',')]
        for i in wpro:
            who_region[i] = 'Western Pacific'

        return who_region
