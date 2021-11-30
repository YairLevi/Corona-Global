import mysql.connector
import pandas as pd

# Globals:
connection = None
cursor = None


# return a dictionary that map each country to her continent and population.
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


# return a dictionary of dynamic variables (msrtype table) and static variables.
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


# get the first and the last date in the DB.
def get_dates() -> dict:
    first = pd.read_sql_query("""SELECT max(msr_timestamp) FROM measurement;""", connection)
    last = pd.read_sql_query("""SELECT min(msr_timestamp) FROM measurement;""", connection)
    my_dict = {'first_date': first, 'last_date': last}
    return my_dict


# given a date, return the new cases, new deaths, total cases, total deaths in this date.
def get_map_variable(date) -> dict:
    dynamic_variables = pd.read_sql_query("""SELECT PKmsr_id, msr_name FROM msrtype;""", connection)
    my_dict = {}
    result_dict = {}

    # create dictionary that map msr_name to her id:
    for row in dynamic_variables.values:
        my_dict[row[1]] = row[0]

    # get the amount of new cases in the given date:
    query = """SELECT sum(msr_value) 
                FROM measurement USE INDEX(searchIndex)
                where msr_timestamp Like "{0}" and FKmsr_id = {1};"""
    query = query.format(date, my_dict['new_cases'])
    new_cases = pd.read_sql_query(query, connection)
    result_dict['new_cases'] = new_cases.values[0][0]

    # get the amount of new deaths in the given date:
    query = """SELECT sum(msr_value) 
                    FROM measurement USE INDEX(searchIndex)
                    where msr_timestamp Like "{0}" and FKmsr_id = {1};"""
    query = query.format(date, my_dict['new_deaths'])
    new_deaths = pd.read_sql_query(query, connection)
    result_dict['new_deaths'] = new_deaths.values[0][0]

    # get the amount of total cases (until and including) the given date:
    query = """SELECT sum(msr_value) 
                        FROM measurement USE INDEX(searchIndex)
                        where msr_timestamp Like "{0}" and FKmsr_id = {1};"""
    query = query.format(date, my_dict['total_cases'])
    total_cases = pd.read_sql_query(query, connection)
    result_dict['total_cases'] = total_cases.values[0][0]

    # get the amount of total deaths (until and including) the given date:
    query = """SELECT sum(msr_value) 
                            FROM measurement USE INDEX(searchIndex)
                            where msr_timestamp Like "{0}" and FKmsr_id = {1};"""
    query = query.format(date, my_dict['total_deaths'])
    total_deaths = pd.read_sql_query(query, connection)
    result_dict['total_deaths'] = total_deaths.values[0][0]
    return result_dict


# given a country and a variable, return a dictionary that maps msr_timestamp to the msr_value in each of the
# timestamps that in the DB. 'variable' is a dynamic variable that his value takes from measurement table.
def get_data_for_scatter_line_graph(country, variable) -> dict:
    query = """SELECT msr_timestamp, msr_value
               FROM measurement
               where FKcountry_id = (select PKcountry_id FROM country where country_name LIKE "{0}") 
               and FKmsr_id = (select PKmsr_id from msrtype where msr_name LIKE "{1}");"""
    query = query.format(country, variable)
    results = pd.read_sql_query(query, connection)

    # create dictionary that maps msr_timestamp to the msr_value in each of the timestamps, in the given country,
    # and given variable.
    country_info = {}
    for row in results.values:
        if row[0].month < 10:
            date = "{0}-0{1}-{2}".format(row[0].year, row[0].month, row[0].day)
        else:
            date = "{0}-{1}-{2}".format(row[0].year, row[0].month, row[0].day)
        country_info[date] = row[1]

    return country_info


# given a country and a variable, return the value of this variable. 'variable' is a static variable
# that takes from country table.
def get_static_data(country, variable):
    query = """SELECT {0}
               FROM country
               where PKcountry_id = (select PKcountry_id FROM country where country_name LIKE "{1}");"""
    query = query.format(variable, country)
    results = pd.read_sql_query(query, connection)
    return results.values[0][0]


# def get_data_for_columns_graph(countries, variable) -> dict:


# return a dictionary that maps each continent to the total deaths from the first date
# until the last date in the continent. This query will display as a column graph.
def total_deaths_in_each_continent():
    results = pd.read_sql_query("""SELECT continent_name, SUM(msr_value) AS total_deaths
                                    FROM measurement, country, msrtype, continent
                                    WHERE measurement.FKcountry_id = country.PKcountry_id
                                    AND measurement.FKmsr_id = msrtype.PKmsr_id
                                    AND country.FKcontinent_id = continent.PKcontinent_id
                                    AND msr_timestamp = (SELECT MAX(msr_timestamp) FROM measurement)
                                    AND FKmsr_id = (SELECT PKmsr_id FROM msrtype WHERE msr_name = 'total_deaths')
                                    GROUP BY continent_name
                                    ORDER BY total_deaths DESC;""", connection)
    my_dict = {}
    for row in results.values:
        my_dict[row[0]] = row[1]
    return my_dict


# percentage cases out of the total population in each continent, according to the last date in the DB.
# This query will display as a column graph.
def percentage_cases_out_of_total_population_in_each_continent():
    results = pd.read_sql_query("""SELECT continent_name, SUM(msr_value) AS total_cases,
                                    SUM(population) AS total_population, 
                                    100*SUM(msr_value)/SUM(population) AS cases_precentage
                                    FROM measurement, country, msrtype, continent
                                    WHERE measurement.FKcountry_id = country.PKcountry_id
                                    AND measurement.FKmsr_id = msrtype.PKmsr_id
                                    AND country.FKcontinent_id = continent.PKcontinent_id
                                    AND msr_timestamp = (SELECT MAX(msr_timestamp) FROM measurement)
                                    AND FKmsr_id = (
                                        SELECT PKmsr_id
                                        FROM msrtype
                                        WHERE msr_name = 'total_cases')
                                    GROUP BY continent_name
                                    ORDER BY cases_precentage DESC
                                    """, connection)

    countries_dict = {}
    for row in results.values:
        countries_dict[row[0]] = {
            'total cases': row[1],
            'total population': row[2],
            'cases percentage': row[3]
        }
    return countries_dict


# find the five countries with the highest human development index, and for each of them return the total deaths
# until the last date in the DB. This query will display as a column graph.
def total_deaths_of_top_five_human_development_index():
    results = pd.read_sql_query("""SELECT DISTINCT country.country_name, developed.human_development_index,
                                    developed.msr_value AS 'total_deaths'
                                    FROM (SELECT DISTINCT PKcountry_id, human_development_index, msr_value
                                     FROM country,measurement, msrtype
                                      WHERE PKcountry_id = FKcountry_id AND FKmsr_id = PKmsr_id AND
                                      FKmsr_id = (SELECT PKmsr_id FROM msrtype WHERE msr_name = 'total_deaths')
                                       AND msr_timestamp = (SELECT MAX(msr_timestamp) FROM measurement) 
                                       ORDER BY human_development_index DESC LIMIT 5) AS developed, measurement, country
                                        WHERE developed.PKcountry_id = measurement.FKcountry_id
                                        AND developed.PKcountry_id = country.PKcountry_id
                                        LIMIT 5;""", connection)
    country_dict = {}
    for row in results.values:
        country_dict[row[0]] = {
            'human_development_index': row[1],
            'total_deaths': row[2]
        }
    return country_dict


# Percentage of all verified deaths out of the total cases, in each of the 5 countries with the highest percentage of
# the population over the age of 70 on the latest date in the DB.
def percentage_of_verified_deaths_out_of_total_cases():
    results = pd.read_sql_query("""SELECT DISTINCT country.country_name, aged.aged_70_older, total_deaths, population, 
                                measurement.msr_value AS total_cases, 
                                100*total_deaths/measurement.msr_value AS deaths_percentage
                                FROM (
                                    SELECT DISTINCT PKcountry_id, aged_70_older, msr_value AS total_deaths
                                    FROM country, measurement, msrtype
                                    WHERE PKcountry_id = FKcountry_id
                                    AND FKmsr_id = PKmsr_id
                                    AND FKmsr_id = (
                                        SELECT PKmsr_id
                                        FROM msrtype
                                        WHERE msr_name = 'total_deaths')
                                    AND msr_timestamp = (SELECT MAX(msr_timestamp) FROM measurement)
                                    ORDER BY aged_70_older DESC
                                    LIMIT 5) AS aged, measurement, country, msrtype
                                WHERE aged.PKcountry_id = measurement.FKcountry_id
                                AND aged.PKcountry_id = country.PKcountry_id
                                AND measurement.FKmsr_id = msrtype.PKmsr_id
                                AND FKmsr_id = (
                                    SELECT PKmsr_id
                                    FROM msrtype
                                    WHERE msr_name = 'total_cases')
                                AND msr_timestamp = (SELECT MAX(msr_timestamp) FROM measurement)
                                ORDER BY deaths_percentage DESC
                                LIMIT 5;
                                """, connection)

    countries_dict = {}
    for row in results.values:
        countries_dict[row[0]] = {
            'aged 70 older': row[1],
            'total deaths': row[2],
            'population': row[3],
            'total cases': row[4],
            'deaths percentage': row[5]
        }
    return countries_dict


# Percentage of verified cases in each continent out of all the global verified cases at the latest date in the DB.
# This query will display as Pie Chart.
def percentage_of_verified_cases_out_of_all_global_verified_cases_for_each_continent():
    results = pd.read_sql_query("""SELECT cases_per_continent.continent_name, 
                                    100*cases_per_continent.total_cases_continent/global_total_cases AS percentage
                                    FROM (
                                        SELECT continent_name, SUM(msr_value) AS total_cases_continent
                                        FROM measurement, country, msrtype, continent
                                        WHERE measurement.FKcountry_id = country.PKcountry_id
                                        AND measurement.FKmsr_id = msrtype.PKmsr_id
                                        AND country.FKcontinent_id = continent.PKcontinent_id
                                        AND msr_timestamp = (SELECT MAX(msr_timestamp) FROM measurement)
                                        AND FKmsr_id = (SELECT PKmsr_id FROM msrtype WHERE msr_name = 'total_cases')
                                        GROUP BY continent_name
                                        ) AS cases_per_continent, (
                                        SELECT SUM(total_cases) AS global_total_cases
                                        FROM (
                                            SELECT continent_name, SUM(msr_value) AS total_cases
                                            FROM measurement, country, msrtype, continent
                                            WHERE measurement.FKcountry_id = country.PKcountry_id
                                            AND measurement.FKmsr_id = msrtype.PKmsr_id
                                            AND country.FKcontinent_id = continent.PKcontinent_id
                                            AND msr_timestamp = (SELECT MAX(msr_timestamp) FROM measurement)
                                            AND FKmsr_id = (SELECT PKmsr_id FROM msrtype WHERE msr_name = 'total_cases')
                                            GROUP BY continent_name
                                        ) AS continental_cases) AS total_continental_cases
                                    ORDER BY percentage DESC
                                    """, connection)
    countries_dict = {}
    for row in results.values:
        countries_dict[row[0]] = row[1]
    return countries_dict


# Queries for update:

# the user wants to upload a new data. For example: Israel, 2020-02-24, 'new_cases', 100.
# We add this data to update table. This data will need to be approved later, by an admin.
# The variable type, must be a type that exists in msrtype table. (the user can't add a new type of measurement).
# Date format that this function get: '2020-02-24'.
def user_update(country_name, date, variable, value):
    country_id_query = """select PKcountry_id FROM country where country_name LIKE '{0}';"""
    country_id_query = country_id_query.format(country_name)
    country_id = pd.read_sql_query(country_id_query, connection).values[0][0]

    msr_id_query = """select PKmsr_id FROM msrtype WHERE msr_name = '{0}';"""
    msr_id_query = msr_id_query.format(variable)
    msr_id = pd.read_sql_query(msr_id_query, connection).values[0][0]

    query = """INSERT INTO measurement_update ({0}) VALUES (%s, %s, %s, %s);"""
    columns = ['FKcountry_id', 'msr_timestamp', 'FKmsr_id', 'msr_value']

    query = query.format(','.join(columns))
    data = [str(country_id), date, str(msr_id), str(value)]
    cursor.execute(query, data)
    connection.commit()
    print("Insert an update for measurement_update table successfully")


# An admin wants to connect to the system, and we need to make sure he is one of the existing admins in the system.
# If this admin exists in the DB return True, otherwise return False.
def check_admin(admin_name, admin_password):
    query = """SELECT EXISTS(select admin_name, admin_pwd
                from admin
                where admin_name = '{0}' and admin_pwd = '{1}')"""
    query = query.format(admin_name, admin_password)
    flag = pd.read_sql_query(query, connection).values[0][0]
    print(flag)
    if flag > 0:
        print("this admin exists in the system")
        return True
    print("this admin doesn't exist in the system")
    return False


# An existing admin wants to add a new measurement type. We add this type to msrtype table.
def add_new_measurement_type(variable_name):
    query = """INSERT INTO msrtype ({0}) VALUES (%s);"""
    query = query.format('msr_name')
    data = [variable_name]
    cursor.execute(query, data)
    connection.commit()
    print("Insert a new measurement type for mstype table successfully")


# An existing admin, clicked on some user updates, and wants to approved them, so he send a list of
# updates, that we will need to delete from update table, and add them to measurements table.
# update_list[i] = (country_name, date, variable, value)
# Note: Date format that this function get: '2020-02-24'.
def confirm_user_update(update_list):
    for row in update_list:
        country_name = row[0]
        date = row[1]
        msr_name = row[2]
        msr_value = row[3]
        query = """select FKcountry_id,msr_timestamp,FKmsr_id,msr_value 
        from measurement_update where FKcountry_id = (select PKcountry_id from country where country_name = '{0}')
         and msr_timestamp = '{1}'
         and FKmsr_id = (select PKmsr_id from msrtype where msr_name = '{2}') and msr_value = {3};"""
        query = query.format(country_name, date, msr_name, msr_value)
        row = pd.read_sql_query(query, connection).values[0]

        # add row to measurement table:
        columns = ['FKcountry_id', 'msr_timestamp', 'FKmsr_id', 'msr_value']
        query = """INSERT INTO measurement ({0}) VALUES (%s, %s, %s, %s);"""
        query = query.format(','.join(columns))
        if row[1].month < 10:
            date = "{0}-0{1}-{2}".format(row[1].year, row[1].month, row[1].day)
        else:
            date = "{0}-{1}-{2}".format(row[1].year, row[1].month, row[1].day)
        data = [row[0], date, row[2], row[3]]
        cursor.execute(query, data)
        connection.commit()

        # delete this row from measurement_update table:
        query = """delete from measurement_update where FKcountry_id = {0} and msr_timestamp = '{1}'
        and FKmsr_id = {2} and msr_value = {3};"""
        query = query.format(row[0], date, row[2], row[3])
        cursor.execute(query)
        connection.commit()

        print("delete row from measurement_update table and add this row to measurement table, successfully")


# Return amount of updates from the update table that will be display for the admin
def get_updates_for_display() -> dict:
    results = pd.read_sql_query("""SELECT DISTINCT country.country_name ,measurement_update.msr_timestamp,
                                msrtype.msr_name, measurement_update.msr_value
                                FROM measurement_update, country, msrtype
                                where country.PKcountry_id = measurement_update.FKcountry_id and 
                                measurement_update.FKmsr_id = msrtype.PKmsr_id
                                LIMIT 1;""", connection)
    my_dict = {}
    for row in results.values:
        if row[1].month < 10:
            date = "{0}-0{1}-{2}".format(row[1].year, row[1].month, row[1].day)
        else:
            date = "{0}-{1}-{2}".format(row[1].year, row[1].month, row[1].day)
        my_dict[row[0]] = {
            'msr_timestamp': date,
            'msr_name': row[2],
            'msr_value': row[3]
        }

    return my_dict


if __name__ == '__main__':
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='covid-19 global data displayer',
                                             user='root',
                                             password='your_password')  # put your MYSQL server password here.

        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

            # total_deaths_in_each_continent()
            # get_map_variable("2021-09-24")
            # total_deaths_of_top_five_human_development_index()
            # get_data_for_scatter_line_graph("Portugal", "new_cases")
            # percentage_cases_out_of_total_population_in_each_continent()
            # percentage_of_verified_deaths_out_of_total_cases()
            # percentage_of_verified_cases_out_of_all_global_verified_cases_for_each_continent()
            # get_static_data("Australia", "population")
            # check_admin('yair', '12')
            # add_new_measurement_type("smoking")
            # get_updates_for_display()
            # user_update("Portugal", "2020-03-19", "new_cases", 100)
            # user_update("Israel", "2020-03-20", "total_cases", 200)
            # confirm_user_update(
            #      [["Portugal", "2020-03-19", "new_cases", '100'], ["Israel", "2020-03-20", "total_cases", '200']])

    except mysql.connector.Error as error:
        print("Error in MySQL: {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
