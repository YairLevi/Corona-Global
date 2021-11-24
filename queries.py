import mysql.connector
import pandas as pd

# Globals:
connection = None
cursor = None


def get_countries() -> dict:
    results = pd.read_sql_query("""SELECT continent.continent_name, country.country_name, country.population 
                                    FROM continent,country
                                    where continent.PKcontinent_id = country.FKcontinent_id;""", connection)
    my_dict = {}
    for row in results.values:
        my_dict[row[1]] = {
            'continent': row[0],
            'population': row[2]
        }
    return my_dict


def get_variables() -> dict:
    dynamic_variables = pd.read_sql_query("""SELECT msr_name FROM msrtype;""", connection)
    static_variables = pd.read_sql_query("""SELECT population_density, median_age, aged_65_older, aged_70_older,
                                            gdp_per_capita, cardiovasc_death_rate, diabetes_prevalence, 
                                            hospital_beds_per_thousand,life_expectancy,human_development_index 
                                            FROM country;""", connection)
    my_dict = {}
    var = []
    for row in dynamic_variables.values:
        var.append(row[0])
    my_dict["dynamic variables"] = var

    var = []
    for row in static_variables.values:
        var.append(row[0])
    my_dict["static variables"] = var

    return my_dict


def get_dates() -> dict:
    first = pd.read_sql_query("""SELECT max(msr_timestamp) FROM measurement;""", connection)
    last = pd.read_sql_query("""SELECT min(msr_timestamp) FROM measurement;""", connection)
    my_dict = {'first_date': first, 'last_date': last}
    return my_dict


def get_map_variable(date) -> dict:
    dynamic_variables = pd.read_sql_query("""SELECT PKmsr_id, msr_name FROM msrtype;""", connection)
    my_dict = {}
    result_dict = {}

    # create dictionary that map msr_name to her id:
    for row in dynamic_variables.values:
        my_dict[row[1]] = row[0]

    # get the amount of new cases in the given date:
    query = """SELECT sum(msr_value) 
                FROM measurement
                where FKmsr_id = {0} and msr_timestamp Like "{1}";"""
    query = query.format(my_dict['new_cases'], date)
    new_cases = pd.read_sql_query(query, connection)
    result_dict['new_cases'] = new_cases.values[0][0]

    # get the amount of new deaths in the given date:
    query = """SELECT sum(msr_value) 
                    FROM measurement
                    where FKmsr_id = {0} and msr_timestamp Like "{1}";"""
    query = query.format(my_dict['new_deaths'], date)
    new_deaths = pd.read_sql_query(query, connection)
    result_dict['new_deaths'] = new_deaths.values[0][0]

    # get the amount of total cases (until and including) the given date:
    query = """SELECT sum(msr_value) 
                        FROM measurement
                        where FKmsr_id = {0} and msr_timestamp Like "{1}";"""
    query = query.format(my_dict['total_cases'], date)
    total_cases = pd.read_sql_query(query, connection)
    result_dict['total_cases'] = total_cases.values[0][0]

    # get the amount of total deaths (until and including) the given date:
    query = """SELECT sum(msr_value) 
                            FROM measurement
                            where FKmsr_id = {0} and msr_timestamp Like "{1}";"""
    query = query.format(my_dict['total_deaths'], date)
    total_deaths = pd.read_sql_query(query, connection)
    result_dict['total_deaths'] = total_deaths.values[0][0]
    print(result_dict)

    return result_dict


# def get_data_for_scatter_line_graph(country, variable) -> dict:

# def get_data_for_columns_graph(countries, variable) -> dict:


if __name__ == '__main__':
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='covid-19 global data displayer',
                                             user='root',
                                             password='put_your_password_here')  # put your MYSQL server password here.

        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

            get_map_variable("2020-02-24")

    except mysql.connector.Error as error:
        print("Error in MySQL: {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
