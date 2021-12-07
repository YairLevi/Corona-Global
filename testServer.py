from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import oop_queries
import mysql.connector
import pandas

encoding = 'utf-8'

def countries(params):
    return queries.get_countries()

def variables(params):
    return queries.get_variables()

def dates(params):
    return queries.get_dates()

def map_variables(params):
    return {'new_cases':1,'total_cases':1,'new_deaths':1,'total_deaths':1}
    # return queries.get_map_variable(connection, params['date'])

def dynamic_var(params):
    return queries.get_data_for_scatter_line_graph(params['country'], params['variable'])

def static_var(params):
    dict = {}
    val = queries.get_static_data(params['country'], params['variable'])
    for date in pandas.date_range(end_dates['first_date'], end_dates['last_date'], freq='d'):
        date_format = date.strftime('%Y-%m-%d')
        dict[date_format] = val
    return dict

def total_deaths_in_each_continent(params):
    return queries.total_deaths_in_each_continent()

def percentage_cases_out_of_total_population_in_each_continent(params):
    return queries.percentage_cases_out_of_total_population_in_each_continent()

def total_deaths_of_top_five_human_development_index(params):
    return queries.total_deaths_of_top_five_human_development_index()

def percentage_of_verified_deaths_out_of_total_cases(params):
    return queries.percentage_of_verified_deaths_out_of_total_cases()

def percentage_of_verified_cases_out_of_all_global_verified_cases_for_each_continent(params):
    return queries.percentage_of_verified_cases_out_of_all_global_verified_cases_for_each_continent()

def check_admin(params):
    return {'is_admin' : queries.check_admin(params['username'], params['password'])}

def get_update_requests(params):
    return queries.get_updates_for_display()

def send_update(params):
    queries.user_update(params['country'], params['date'], params['variable'], params['value'])

def add_msr(params):
    queries.add_new_measurement_type(params['msr'])

def approve(params):
    queries.confirm_user_update([[params['country'], params['date'], params['variable'], params['value']]])

def deny(params):
    queries.reject_user_update([[params['country'], params['date'], params['variable'], params['value']]])

routes_GET = {
    '/countries': countries,
    '/variables': variables,
    '/dates': dates,
    '/map': map_variables,
    '/var/dynamic': dynamic_var,
    '/var/static': static_var,
    '/case_percentage_population': percentage_cases_out_of_total_population_in_each_continent,
    '/case_percentage_global': percentage_of_verified_cases_out_of_all_global_verified_cases_for_each_continent,
    '/death_percentage': percentage_of_verified_deaths_out_of_total_cases,
    '/admin': check_admin,
    '/updates': get_update_requests,
    '/update': send_update,
    '/addmsr': add_msr,
    '/approve': approve,
    '/deny': deny,
}

class Server(SimpleHTTPRequestHandler):

    def __init__(self, request: bytes, client_address, server):
        super().__init__(request, client_address, server)

    def _set_headers(self):
        self.send_response(200)
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def get_query_params(self, string):
        string = string.replace('%20', ' ')
        params = string.split('&')
        pDict = {}
        for p in params:
            if p == '': continue
            pair = p.split('=')
            pDict[pair[0]] = pair[1]
        return pDict

    def do_GET(self):
        self._set_headers()
        if self.path == '/favicon.ico': return
        if self.path == '/': self.path = '/index.html'
        params = {}
        if '?' in self.path:
            l = self.path.split('?')
            self.path = l[0]
            params = self.get_query_params(l[1])
        try:
            g = routes_GET[self.path](params)
            print(g)
            data = json.dumps(g)
            self.wfile.write(bytes(data, encoding))
        except:
            with open(self.path[1:], 'rb') as f:
                content = f.read()
                f.close()
            self.wfile.write(content)


# try:
#     connection = mysql.connector.connect(host='localhost',
#                                          database='covid-19 global data displayer',
#                                          user='root',
#                                          password='240301Yl')  # put your MYSQL server password here.
#     if connection.is_connected():
#         db_Info = connection.get_server_info()
#         print("Connected to MySQL Server version ", db_Info)
#         cursor = connection.cursor()
#         cursor.execute("select database();")
#         record = cursor.fetchone()
#         print("You're connected to database: ", record)
# except mysql.connector.Error as error:
#     print("Error in MySQL: {}".format(error))

queries = oop_queries.Queries()
queries.connect()
end_dates = dates({})
httpServer = HTTPServer(('localhost', 8000), Server)
print('Server is running at http://localhost:8000/')
httpServer.serve_forever()
