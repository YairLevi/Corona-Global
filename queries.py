import mysql.connector
import pandas as pd

# Globals:
connection = None
cursor = None


def get_countries() -> dict:
    results = pd.read_sql_query("""SELECT continent.continent_name, country.country_name, country.population 
                                    FROM continent,country
                                    where continent.PKcontinent_id = country.FKcontinent_id;""", connection)
    dict = {}
    for row in results.values:
        dict[row[1]] = {
            'continent': row[0],
            'population': row[2]
        }
    return dict


def get_variables() -> dict:
    results = pd.read_sql_query("""SELECT msr_name FROM msrtype;""", connection)
    dict = {}
    var = []
    for row in results.values:
        var.append(row[0])
    dict["variables"] = var
    return dict


def get_dates() -> dict:
    max = pd.read_sql_query("""SELECT max(msr_timestamp) FROM measurement;""", connection)
    min = pd.read_sql_query("""SELECT min(msr_timestamp) FROM measurement;""", connection)
    dict = {}
    dict['first_date'] = min
    dict['last_date'] = max
    return dict


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

    except mysql.connector.Error as error:
        print("Error in MySQL: {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
