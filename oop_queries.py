import mysql.connector
import pandas as pd
import sys


class Queries:
    def __init__(self):
        self.__connection = None
        self.__cursor = None

    def connect(self):
        try:
            self.__connection = mysql.connector.connect(host='localhost',
                                                        database='covid-19 global data displayer',
                                                        user='root',
                                                        password=sys.argv[1])  # put your MYSQL server password here.

            if self.__connection.is_connected():
                db_Info = self.__connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                self.__cursor = self.__connection.cursor()
                self.__cursor.execute("select database();")
                record = self.__cursor.fetchone()
                print("You're connected to database: ", record)

        except mysql.connector.Error as error:
            print("Error in connect: {}".format(error))

    def close(self):
        if self.__connection.is_connected():
            self.__cursor.close()
            self.__connection.close()
            print("MySQL connection is closed")

    # return a dictionary that map each country to her continent and population.
    def get_countries(self) -> dict:
        try:
            results = pd.read_sql_query("""SELECT continent.continent_name, country.country_name, country.population 
                                           FROM continent,country
                                           where continent.PKcontinent_id = country.FKcontinent_id;""",
                                        self.__connection)
            my_dict = {}
            for row in results.values:
                my_dict[row[1]] = {
                    'continent': row[0],
                    'population': row[2]
                }
            return my_dict
        except mysql.connector.Error as error:
            print("Error in get_countries: {}".format(error))
            self.close()

    # return a dictionary of dynamic variables (msrtype table) and static variables.
    def get_variables(self) -> dict:
        try:
            dynamic_variables = pd.read_sql_query("""SELECT msr_name FROM msrtype;""", self.__connection)

            my_dict = {}
            var = []
            for row in dynamic_variables.values:
                var.append(row[0])
            my_dict["dynamic_variables"] = var

            var = ['population_density', 'median_age', 'aged_65_older', 'aged_70_older',
                   'gdp_per_capita', 'cardiovasc_death_rate', 'diabetes_prevalence',
                   'hospital_beds_per_thousand', 'life_expectancy', 'human_development_index']
            my_dict["static_variables"] = var

            return my_dict

        except mysql.connector.Error as error:
            print("Error in get_variables: {}".format(error))
            self.close()

    def change_date_format(self, date):
        if date is not None:
            if date.month < 10:
                date = "{0}-0{1}-{2}".format(date.year, date.month, date.day)
            else:
                date = "{0}-{1}-{2}".format(date.year, date.month, date.day)
            return date

    # get the first and the last date in the DB.
    def get_dates(self) -> dict:
        try:
            last = pd.read_sql_query("""SELECT max(msr_timestamp) FROM measurement;""", self.__connection).values[0][0]
            first = pd.read_sql_query("""SELECT min(msr_timestamp) FROM measurement;""", self.__connection).values[0][0]

            my_dict = {'first_date': self.change_date_format(first), 'last_date': self.change_date_format(last)}
            return my_dict

        except mysql.connector.Error as error:
            print("Error in get_dates: {}".format(error))
            self.close()

    # given a date, return the new cases, new deaths, total cases, total deaths in this date.
    def get_map_variable(self, date) -> dict:
        try:
            dynamic_variables = pd.read_sql_query("""SELECT PKmsr_id, msr_name FROM msrtype;""", self.__connection)
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
            new_cases = pd.read_sql_query(query, self.__connection)
            result_dict['new_cases'] = new_cases.values[0][0]

            # get the amount of new deaths in the given date:
            query = """SELECT sum(msr_value) 
                                    FROM measurement USE INDEX(searchIndex)
                                    where msr_timestamp Like "{0}" and FKmsr_id = {1};"""
            query = query.format(date, my_dict['new_deaths'])
            new_deaths = pd.read_sql_query(query, self.__connection)
            result_dict['new_deaths'] = new_deaths.values[0][0]

            # get the amount of total cases (until and including) the given date:
            query = """SELECT sum(msr_value) 
                                        FROM measurement USE INDEX(searchIndex)
                                        where msr_timestamp Like "{0}" and FKmsr_id = {1};"""
            query = query.format(date, my_dict['total_cases'])
            total_cases = pd.read_sql_query(query, self.__connection)
            result_dict['total_cases'] = total_cases.values[0][0]

            # get the amount of total deaths (until and including) the given date:
            query = """SELECT sum(msr_value) 
                                            FROM measurement USE INDEX(searchIndex)
                                            where msr_timestamp Like "{0}" and FKmsr_id = {1};"""
            query = query.format(date, my_dict['total_deaths'])
            total_deaths = pd.read_sql_query(query, self.__connection)
            result_dict['total_deaths'] = total_deaths.values[0][0]
            return result_dict

        except mysql.connector.Error as error:
            print("Error in get_map_variable: {}".format(error))
            self.close()

    # given a country and a variable, return a dictionary that maps msr_timestamp to the msr_value in each of the
    # timestamps that in the DB. 'variable' is a dynamic variable that his value takes from measurement table.
    def get_data_for_scatter_line_graph(self, country, variable) -> dict:
        try:
            query = """SELECT msr_timestamp, msr_value
                               FROM measurement
                               where FKcountry_id = (select PKcountry_id FROM country where country_name LIKE "{0}") 
                               and FKmsr_id = (select PKmsr_id from msrtype where msr_name LIKE "{1}");"""
            query = query.format(country, variable)
            results = pd.read_sql_query(query, self.__connection)

            # create dictionary that maps msr_timestamp to the msr_value in each of the timestamps, in the given
            # country, and given variable.
            country_info = {}
            for row in results.values:
                if row[0].month < 10:
                    date = "{0}-0{1}-{2}".format(row[0].year, row[0].month, row[0].day)
                else:
                    date = "{0}-{1}-{2}".format(row[0].year, row[0].month, row[0].day)
                country_info[date] = row[1]

            return country_info

        except mysql.connector.Error as error:
            print("Error in get_data_for_scatter_line_graph: {}".format(error))
            self.close()

    # given a country and a variable, return the value of this variable. 'variable' is a static variable
    # that takes from country table.
    def get_static_data(self, country, variable):
        try:
            query = """SELECT {0}
                               FROM country
                               where PKcountry_id = (select PKcountry_id FROM country where country_name LIKE "{1}");"""
            query = query.format(variable, country)
            results = pd.read_sql_query(query, self.__connection)
            return results.values[0][0]

        except mysql.connector.Error as error:
            print("Error in get_static_data: {}".format(error))
            self.close()

    # return a dictionary that maps each continent to the total deaths from the first date
    # until the last date in the continent. This query will display as a column graph.
    def total_deaths_in_each_continent(self):
        try:
            results = pd.read_sql_query("""SELECT continent_name, SUM(msr_value) AS total_deaths
                                                    FROM measurement, country, msrtype, continent
                                                    WHERE measurement.FKcountry_id = country.PKcountry_id
                                                    AND measurement.FKmsr_id = msrtype.PKmsr_id
                                                    AND country.FKcontinent_id = continent.PKcontinent_id
                                                    AND msr_timestamp = (SELECT MAX(msr_timestamp) FROM measurement)
                                                    AND FKmsr_id = (SELECT PKmsr_id FROM msrtype WHERE msr_name = 'total_deaths')
                                                    GROUP BY continent_name
                                                    ORDER BY total_deaths DESC;""", self.__connection)
            my_dict = {}
            for row in results.values:
                my_dict[row[0]] = row[1]
            return my_dict
        except mysql.connector.Error as error:
            print("Error in total_deaths_in_each_continent: {}".format(error))
            self.close()

    # percentage cases out of the total population in each continent, according to the last date in the DB.
    # This query will display as a column graph.
    def percentage_cases_out_of_total_population_in_each_continent(self):
        try:
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
                                                    """, self.__connection)

            continent_dict = {}
            for row in results.values:
                continent_dict[row[0]] = {
                    'total_cases': row[1],
                    'total_population': row[2],
                    'cases_percentage': row[3]
                }
            return continent_dict
        except mysql.connector.Error as error:
            print("Error in percentage_cases_out_of_total_population_in_each_continent: {}".format(error))
            self.close()

    # find the five countries with the highest human development index, and for each of them return the total deaths
    # until the last date in the DB. This query will display as a column graph.
    def total_deaths_of_top_five_human_development_index(self):
        try:
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
                                                        LIMIT 5;""", self.__connection)
            country_dict = {}
            for row in results.values:
                country_dict[row[0]] = {
                    'human_development_index': row[1],
                    'total_deaths': row[2]
                }
            return country_dict

        except mysql.connector.Error as error:
            print("Error in total_deaths_of_top_five_human_development_index: {}".format(error))
            self.close()

    # Percentage of all verified deaths out of the total cases, in each of the 5 countries with the highest
    # percentage of the population over the age of 70 on the latest date in the DB.
    def percentage_of_verified_deaths_out_of_total_cases(self):
        try:
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
                                                """, self.__connection)

            countries_dict = {}
            for row in results.values:
                countries_dict[row[0]] = {
                    'aged_70_older': row[1],
                    'total_deaths': row[2],
                    'population': row[3],
                    'total_cases': row[4],
                    'deaths_percentage': row[5]
                }
            return countries_dict

        except mysql.connector.Error as error:
            print("Error in percentage_of_verified_deaths_out_of_total_cases: {}".format(error))
            self.close()

    # Percentage of verified cases in each continent out of all the global verified cases at the latest date in the DB.
    # This query will display as Pie Chart.
    def percentage_of_verified_cases_out_of_all_global_verified_cases_for_each_continent(self):
        try:
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
                                                    """, self.__connection)
            continent_dict = {}
            for row in results.values:
                continent_dict[row[0]] = row[1]
            return continent_dict
        except mysql.connector.Error as error:
            print(
                "Error in percentage_of_verified_cases_out_of_all_global_verified_cases_for_each_continent: {}".format(
                    error))
            self.close()

    # Queries for update:

    # the user wants to upload a new data. For example: Israel, 2020-02-24, 'new_cases', 100.
    # We add this data to update table. This data will need to be approved later, by an admin.
    # The variable type, must be a type that exists in msrtype table. (the user can't add a new type of measurement).
    # Date format that this function get: '2020-02-24'.
    def user_update(self, country_name, date, variable, value):
        try:
            country_id_query = """select PKcountry_id FROM country where country_name LIKE '{0}';"""
            country_id_query = country_id_query.format(country_name)
            country_id = pd.read_sql_query(country_id_query, self.__connection).values[0][0]

            msr_id_query = """select PKmsr_id FROM msrtype WHERE msr_name = '{0}';"""
            msr_id_query = msr_id_query.format(variable)
            msr_id = pd.read_sql_query(msr_id_query, self.__connection).values[0][0]

            query = """INSERT INTO measurement_update ({0}) VALUES (%s, %s, %s, %s);"""
            columns = ['FKcountry_id', 'msr_timestamp', 'FKmsr_id', 'msr_value']

            query = query.format(','.join(columns))
            data = [str(country_id), date, str(msr_id), str(value)]
            self.__cursor.execute(query, data)
            self.__connection.commit()
            print("Insert an update for measurement_update table successfully")

        except mysql.connector.Error as error:
            print("Error in user_update: {}".format(error))
            self.close()

    # An admin wants to connect to the system, and we need to make sure he is one of the existing admins in the system.
    # If this admin exists in the DB return True, otherwise return False.
    def check_admin(self, admin_name, admin_password):
        try:
            query = """SELECT EXISTS(select admin_name, admin_pwd
                                from admin
                                where admin_name = '{0}' and admin_pwd = '{1}')"""
            query = query.format(admin_name, admin_password)
            flag = pd.read_sql_query(query, self.__connection).values[0][0]
            print(flag)
            if flag > 0:
                print("this admin exists in the system")
                return True
            print("this admin doesn't exist in the system")
            return False
        except mysql.connector.Error as error:
            print("Error in check_admin: {}".format(error))
            self.close()

    # An existing admin wants to add a new measurement type. We add this type to msrtype table.
    def add_new_measurement_type(self, variable_name):
        try:
            query = """INSERT INTO msrtype ({0}) VALUES (%s);"""
            query = query.format('msr_name')
            data = [variable_name]
            self.__cursor.execute(query, data)
            self.__connection.commit()
            print("Insert a new measurement type for mstype table successfully")
        except mysql.connector.Error as error:
            print("Error in add_new_measurement_type: {}".format(error))
            self.close()

    # An existing admin, clicked on some user updates, and wants to approved them, so he send a list of
    # updates, that we will need to delete from update table, and add them to measurements table.
    # update_list[i] = (country_name, date, variable, value)
    # Note: Date format that this function get: '2020-02-24'.
    def confirm_user_update(self, update_list):
        try:
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
                row = pd.read_sql_query(query, self.__connection).values[0]

                # add row to measurement table:
                columns = ['FKcountry_id', 'msr_timestamp', 'FKmsr_id', 'msr_value']
                query = """INSERT INTO measurement ({0}) VALUES (%s, %s, %s, %s);"""
                query = query.format(','.join(columns))
                if row[1].month < 10:
                    date = "{0}-0{1}-{2}".format(row[1].year, row[1].month, row[1].day)
                else:
                    date = "{0}-{1}-{2}".format(row[1].year, row[1].month, row[1].day)
                data = [row[0], date, row[2], row[3]]
                self.__cursor.execute(query, data)
                self.__connection.commit()

                # delete this row from measurement_update table:
                query = """delete from measurement_update where FKcountry_id = {0} and msr_timestamp = '{1}'
                and FKmsr_id = {2} and msr_value = {3};"""
                query = query.format(row[0], date, row[2], row[3])
                self.__cursor.execute(query)
                self.__connection.commit()

                print("delete row from measurement_update table and add this row to measurement table, successfully")

        except mysql.connector.Error as error:
            print("Error in confirm_user_update: {}".format(error))
            self.close()

    # Return amount of updates from the update table that will be display for the admin
    def get_updates_for_display(self) -> dict:
        try:
            amount_of_rows_in_table = \
                pd.read_sql_query("""SELECT count(*) from measurement_update;""", self.__connection).values[0][0]
            if amount_of_rows_in_table < 10:
                amount_of_updates_for_display = amount_of_rows_in_table
            else:
                amount_of_updates_for_display = 10

            query = """SELECT DISTINCT country.country_name ,measurement_update.msr_timestamp,
                                                msrtype.msr_name, measurement_update.msr_value
                                                FROM measurement_update, country, msrtype
                                                where country.PKcountry_id = measurement_update.FKcountry_id and 
                                                measurement_update.FKmsr_id = msrtype.PKmsr_id
                                                LIMIT {0};"""
            query = query.format(amount_of_updates_for_display)
            results = pd.read_sql_query(query, self.__connection)

            my_dict = {}
            for row in results.values:
                if row[1].month < 10:
                    date = "{0}-0{1}-{2}".format(row[1].year, row[1].month, row[1].day)
                else:
                    date = "{0}-{1}-{2}".format(row[1].year, row[1].month, row[1].day)

                # my_dict[country] = [dict1, dict2, ... , dict_k]
                # (if this country has k measurement's updates in the DB).
                # each value in the list will be a dictionary that represent an update of the same country in the DB.

                # check if we already have this country as a key:
                if row[0] in my_dict:
                    my_dict[row[0]].append({
                        'msr_timestamp': date,
                        'msr_name': row[2],
                        'msr_value': row[3]
                    })
                else:
                    my_dict[row[0]] = [{
                        'msr_timestamp': date,
                        'msr_name': row[2],
                        'msr_value': row[3]
                    }]

            return my_dict

        except mysql.connector.Error as error:
            print("Error in get_updates_for_display: {}".format(error))
            self.close()

    # An existing admin, clicked on some user updates, and wants to reject them, so he send a list of
    # updates, that we will need to delete from update table, and add them to measurements table.
    # update_list[i] = (country_name, date, variable, value)
    # Note: Date format that this function get: '2020-02-24'.
    def reject_user_update(self, update_list):
        try:
            for row in update_list:
                country_name = row[0]
                date = row[1]
                msr_name = row[2]
                msr_value = row[3]

                # delete this row from measurement_update table:
                query = """delete from measurement_update 
                            where FKcountry_id = (select PKcountry_id from country where country_name = '{0}') 
                            and msr_timestamp = '{1}'
                                and FKmsr_id = (select PKmsr_id from msrtype where msr_name = '{2}') 
                                and msr_value = {3};"""
                query = query.format(country_name, date, msr_name, msr_value)
                self.__cursor.execute(query)
                self.__connection.commit()

        except mysql.connector.Error as error:
            print("Error in reject_user_update: {}".format(error))
            self.close()
