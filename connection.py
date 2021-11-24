import csv
import mysql.connector
import pandas as pd
import os


# Given a cursor, a db_table_name, and q query --> Check if there is a table in the DB with 'db_table_name' name
# and if so throw it and then create a new one in the DB.
def create_table(my_cursor, db_table_name, query):
    drop_query = """DROP TABLE IF EXISTS {0};""".format(db_table_name)
    my_cursor.execute(drop_query)
    print('Creating table: ' + db_table_name)
    my_cursor.execute(query)
    print(db_table_name + " Table created successfully")


# csv_name - the name of your csv file.
# table_name - the name of the table in your DB.
# my_cursor - your program cursor.
# Note: You must have the column names in your csv file that match the columns names of the table
# that you have created in your DB.
def insert_into_table(csv_name, table_name, my_cursor, my_connection):
    with open(csv_name, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        columns = next(reader)
        my_list = []
        for i in range(len(columns)):
            my_list.append('%s')
        query = """INSERT INTO {0} ({1}) VALUES ({2});"""
        query = query.format(table_name, ','.join(columns), ','.join(my_list))

        for data in reader:
            data = [None if v == '' else v for v in data]
            if data[0] is None:
                continue
            if 'World' in data:
                continue

            # change the format of the date (for the measurements table). data is a row form ths csv file.
            # In measurement table: (data[1] = date) --> we want to change the date format.
            # for example: 24/02/2020 --> 2020-02-24.
            if len(data) > 1 and ('/' in data[1]):
                data[1] = data[1].replace("/", "-")
                my_list = data[1].split("-")
                data[1] = my_list[2] + "-" + my_list[1] + "-" + my_list[0]

            my_cursor.execute(query, data)
        my_connection.commit()


# we create another table that connect between country and continent --> in order to find the FK for
# the country_table. Finally we drop this table (that assign each country it's continent)
def calc_fk_for_country_table(my_cursor, my_connection, csv_name):
    create_table(cursor, 'continent_to_country', """CREATE TABLE `covid-19 global data displayer`.`continent_to_country` (
                                                      `continent_name` VARCHAR(45) NULL,
                                                      `country_name` VARCHAR(45) NULL,
                                                      `id` INT NOT NULL AUTO_INCREMENT,
                                                      PRIMARY KEY (`id`));""")
    insert_into_table(csv_name, 'continent_to_country', my_cursor, my_connection)
    results = pd.read_sql_query("""SELECT PKcontinent_id, country_name from continent,continent_to_country
                                where continent.continent_name = continent_to_country.continent_name; """
                                , my_connection)
    drop_query = """DROP TABLE IF EXISTS {0};""".format('continent_to_country')
    my_cursor.execute(drop_query)
    results.to_csv('combined.csv', index=False)

    with open('combined.csv', 'r') as f:
        reader = csv.reader(f)
        dict = {rows[1]: rows[0] for rows in reader}

    df = pd.read_csv('Countries.csv')
    df["FKcontinent_id"] = df["country_name"]
    df["FKcontinent_id"] = df["FKcontinent_id"].map(dict)
    df.to_csv('Countries.csv', index=False, header=True)
    delete_file('combined.csv')
    # delete_file('continent_to_country.csv')


# delete a given file.
def delete_file(file):
    if os.path.exists(file) and os.path.isfile(file):
        os.remove(file)
        print("file deleted")
    else:
        print("file not found")


# calc the FKmsr_id and the FKcountry_id for measurements_table.
def set_fk_for_measurements_table(my_cursor, my_connection, csv_name):
    # calc the FKcountry_id:
    results = pd.read_sql_query("""SELECT PKcountry_id, country_name from country; """, my_connection)

    # create dictionary that map country to her id.
    results.to_csv('combined.csv', index=False)
    with open('combined.csv', 'r') as f:
        reader = csv.reader(f)
        dict = {rows[1]: rows[0] for rows in reader}

    df = pd.read_csv('measurements.csv')
    df['FKcountry_id'] = df['FKcountry_id'].map(dict)
    df.to_csv(csv_name, index=False, header=True)
    delete_file('combined.csv')

    # calc the FKmsr_id:
    results = pd.read_sql_query("""SELECT PKmsr_id, msr_name from msrtype; """, my_connection)

    # create dictionary that msr_name to her id.
    results.to_csv('combined.csv', index=False)
    with open('combined.csv', 'r') as f:
        reader = csv.reader(f)
        dict = {rows[1]: rows[0] for rows in reader}

    df = pd.read_csv(csv_name)
    df['FKmsr_id'] = df['FKmsr_id'].map(dict)
    df.to_csv(csv_name, index=False, header=True)
    delete_file('combined.csv')


# check if one of the msr_value in measurement's table is below 0 and if so set msr_value = 0.
def add_trigger_to_measurements_table(my_cursor, my_connection):
    my_cursor.execute("drop trigger if exists measurements_trigger")
    query = "CREATE TRIGGER measurements_trigger" \
            " BEFORE INSERT ON measurement" \
            " FOR EACH ROW" \
            " BEGIN" \
            " IF NEW.msr_value < 0 THEN" \
            " SET NEW.msr_value = 0; END IF; END; "
    my_cursor.execute(query)
    my_connection.commit()


# Connect to MYSQL server, creates tables, and upload them to the server, and insert values to them.
if __name__ == '__main__':
    connection = None
    cursor = None
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

            # creates tables:
            cursor.execute('SET FOREIGN_KEY_CHECKS = 0;')
            create_table(cursor, 'continent', """CREATE TABLE `covid-19 global data displayer`.`continent` (
                                                `PKcontinent_id` TINYINT NOT NULL AUTO_INCREMENT,
                                                `continent_name` VARCHAR(45) NULL,
                                                 PRIMARY KEY (`PKcontinent_id`)); """)
            # insert values to table:
            insert_into_table('Continents.csv', 'continent', cursor, connection)
            print("Insert values to continent table successfully")

            # calculate FK for country table:
            calc_fk_for_country_table(cursor, connection, 'continent_to_country.csv')

            create_table(cursor, 'country', """CREATE TABLE `covid-19 global data displayer`.`country` (
                                              `PKcountry_id` INT NOT NULL AUTO_INCREMENT,
                                              `FKcontinent_id` TINYINT NULL,
                                              `country_name` VARCHAR(45) NULL,
                                              `population` INT NULL,
                                              `population_density` FLOAT NULL,
                                              `median_age` FLOAT NULL,
                                              `aged_65_older` FLOAT NULL,
                                              `aged_70_older` FLOAT NULL,
                                              `gdp_per_capita` DOUBLE NULL,
                                              `cardiovasc_death_rate` FLOAT NULL,
                                              `diabetes_prevalence` FLOAT NULL,
                                              `hospital_beds_per_thousand` FLOAT NULL,
                                              `life_expectancy` FLOAT NULL,
                                              `human_development_index` FLOAT NULL,
                                              PRIMARY KEY (`PKcountry_id`),
                                              INDEX `FKcontinent_id_idx` (`FKcontinent_id` ASC) VISIBLE,
                                              CONSTRAINT `FKcontinent_id`
                                            FOREIGN KEY (`FKcontinent_id`)
                                            REFERENCES `covid-19 global data displayer`.`continent` (`PKcontinent_id`)
                                                ON DELETE RESTRICT
                                                ON UPDATE RESTRICT); """)
            # insert values to table:
            insert_into_table('Countries.csv', 'country', cursor, connection)
            print("Insert values to country table successfully")

            create_table(cursor, 'msrtype', """CREATE TABLE `covid-19 global data displayer`.`msrtype` (
                                          `PKmsr_id` INT NOT NULL AUTO_INCREMENT,
                                          `msr_name` VARCHAR(45) NULL,
                                          PRIMARY KEY (`PKmsr_id`)); """)
            # insert values to table:
            insert_into_table('msrType.csv', 'msrtype', cursor, connection)
            print("Insert values to msrtype table successfully")

            # set FK for measurements_table
            set_fk_for_measurements_table(cursor, connection, 'measurements.csv')

            create_table(cursor, 'measurement', """CREATE TABLE `covid-19 global data displayer`.`measurement` (
                                                          `PKmeasurement_id` INT NOT NULL AUTO_INCREMENT,
                                                          `FKcountry_id` INT NULL,
                                                          `msr_timestamp` DATE NULL,
                                                          `FKmsr_id` INT NULL,
                                                          `msr_value` FLOAT NULL,
                                                          PRIMARY KEY (`PKmeasurement_id`),
                                                          INDEX `FKcountry_id_idx` (`FKcountry_id` ASC) VISIBLE,
                                                          INDEX `FKmsr_id_idx` (`FKmsr_id` ASC) VISIBLE,
                                                          CONSTRAINT `FKcountry_id`
                                                            FOREIGN KEY (`FKcountry_id`)
                                                            REFERENCES `covid-19 global data displayer`.`country` (`PKcountry_id`)
                                                            ON DELETE RESTRICT
                                                            ON UPDATE RESTRICT,
                                                          CONSTRAINT `FKmsr_id`
                                                            FOREIGN KEY (`FKmsr_id`)
                                                            REFERENCES `covid-19 global data displayer`.`msrtype` (`PKmsr_id`)
                                                            ON DELETE RESTRICT
                                                            ON UPDATE RESTRICT);
                                                         """)

            add_trigger_to_measurements_table(cursor, connection)

            # insert values to table:
            insert_into_table('measurements.csv', 'measurement', cursor, connection)
            print("Insert values to measurement table successfully")

            create_table(cursor, 'admin', """CREATE TABLE `covid-19 global data displayer`.`admin` (
                                              `PKadmin_id` INT NOT NULL AUTO_INCREMENT,
                                              `admin_name` VARCHAR(45) NULL,
                                              `admin_pwd` VARCHAR(45) NULL,
                                              PRIMARY KEY (`PKadmin_id`));
                                                                     """)

            cursor.execute('SET FOREIGN_KEY_CHECKS = 1;')

    except mysql.connector.Error as error:
        print("Error in MySQL: {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
