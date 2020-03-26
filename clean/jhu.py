import os
import pandas as pd


class jhu:
    @staticmethod
    def get_data():
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
        df_1['Province'] = df_1['Province/State']
        del df_1['Province/State']
        df_1['Country'] = df_1['Country/Region']
        del df_1['Country/Region']
        df_1['Update'] = df_1['Last Update']
        del df_1['Last Update']

        df_2['Confirmed'].fillna(0, inplace=True)
        df_2['Deaths'].fillna(0, inplace=True)
        df_2['Recovered'].fillna(0, inplace=True)
        df_2['State'] = df_2['Province/State']
        del df_2['Province/State']
        df_2['Country'] = df_2['Country/Region']
        del df_2['Country/Region']
        df_2['Update'] = df_2['Last Update']
        del df_2['Last Update']

        df_3['Confirmed'].fillna(0, inplace=True)
        df_3['Deaths'].fillna(0, inplace=True)
        df_3['Recovered'].fillna(0, inplace=True)
        df_3['Latitude'] = df_3['Lat']
        del df_3['Lat']
        df_3['Longitude'] = df_3['Long_']
        df_3['Update'] = df_3['Last_Update']
        del df_3['Last_Update']
        del df_3['Long_']
        del df_3['FIPS']
        df_3['City'] = df_3['Admin2']
        del df_3['Admin2']
        del df_3['Combined_Key']
        del df_3['Active']

        # Merge Dataframes into one Big to write it to a CSV file
        columns = ['City', 'State', 'Country', 'Update', 'Latitude', 'Longitude',
                   'Confirmed', 'Deaths', 'Recovered']
        frames = [df_1, df_2, df_3]
        df = pd.DataFrame(pd.concat(frames), columns=columns)
        df.reset_index(inplace=True, drop=True)
        df['City'].fillna('', inplace=True)
        df['State'].fillna('', inplace=True)
        csv = 'data/jhu/time_series_confirmed_deaths_recovered.csv'
        df.to_csv(csv)
        print('Create file ' + csv + '\n')
