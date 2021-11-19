import pandas as pd
import numpy as np

pd.options.mode.chained_assignment = None  # default='warn'


# create countries table.
def create_countries(file_name, columns, table_name):
    df = pd.read_csv(file_name)
    split_df = df[columns]
    split_df.drop_duplicates(subset=None, inplace=True)
    split_df.rename(columns={"continent": "FKcontinent_id", "name": "country_name"}, inplace=True)
    split_df.to_csv(table_name, index=False)


# create continents table.
def create_continents(file_name, columns, table_name):
    df = pd.read_csv(file_name)
    split_df = df[columns]
    split_df.rename(columns={"continent": "continent_name"}, inplace=True)
    split_df.drop_duplicates(subset=None, inplace=True)
    split_df.dropna().to_csv(table_name, index=False)  # dropna() drop rows with null values.


# create a table that map each country to her continent.
def create_continent_to_country(file_name, columns, table_name):
    df = pd.read_csv(file_name)
    split_df = df[columns]
    split_df.rename(columns={"continent": "continent_name", "name": "country_name"}, inplace=True)
    split_df.drop_duplicates(subset=None, inplace=True)
    split_df.dropna().to_csv(table_name, index=False)  # dropna() drop rows with null values.


# create measurements types table.
def create_msrtype_table(file_name, table_name):
    df = pd.DataFrame(['new_cases', 'new_deaths', 'reproduction_rate', 'stringency_index', 'total_cases',
                       'total_deaths'], columns=['msr_name'])
    df.to_csv('msrType.csv', index=False)


# create measurements table.
def create_measurements_table(file_name, table_name):
    df = pd.read_csv(file_name)
    msr_type_list = ['name', 'date', 'new_cases', 'new_deaths', 'reproduction_rate', 'stringency_index', 'total_cases',
                     'total_deaths']
    split_df = df[msr_type_list]

    split_df_transposed = split_df.T

    # put the headers just in the first time appending, and after that append data to the measurements csv file
    # without the headers.
    is_header_first_time = True

    for i, column in enumerate(split_df_transposed):
        row = np.asarray(split_df_transposed[column])
        df1 = pd.DataFrame([[row[0], row[1]]], columns=['FKcountry_id', 'msr_timestamp'])
        d = {'FKmsr_id': [msr_type_list[i] for i in range(2, len(msr_type_list))],
             'msr_value': [row[i] for i in range(2, len(row))]}
        df2 = pd.DataFrame(data=d)
        df_merge = df1.merge(df2, how='cross')
        if is_header_first_time:
            df_merge.dropna().to_csv(table_name, mode='a')  # dropna() drop rows with null values.
            is_header_first_time = False
        else:
            df_merge.dropna().to_csv(table_name, mode='a', header=False)  # dropna() drop rows with null values.

    df = pd.read_csv(table_name)
    first_column = df.columns[0]
    # Delete first column
    df = df.drop([first_column], axis=1)
    df.to_csv(table_name, index=False)


# Given the original csv file, we create several csv files for the requested tables in our DB.
if __name__ == '__main__':
    create_countries('covid_data_set_OWID.csv',
                     ['continent', 'name', 'population', 'population_density', 'median_age', 'aged_65_older',
                      'aged_70_older',
                      'gdp_per_capita',
                      'cardiovasc_death_rate', 'diabetes_prevalence', 'hospital_beds_per_thousand',
                      'life_expectancy', 'human_development_index'], 'Countries.csv')

    create_continents('covid_data_set_OWID.csv', ['continent'], 'Continents.csv')

    create_continent_to_country('covid_data_set_OWID.csv', ['continent', 'name'],
                                'continent_to_country.csv')

    create_msrtype_table('covid_data_set_OWID.csv', 'msrType.csv')

    create_measurements_table('covid_data_set_OWID.csv', 'measurements.csv')
