from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import q

encoding = 'utf-8'

def getIndex(server: SimpleHTTPRequestHandler, path: str):
    with open('index.html', 'r') as file:
        content = file.read()
        server.wfile.write(bytes(content, encoding))
    file.close()

def get_countries(server: SimpleHTTPRequestHandler, path: str):
    j = {
        "United States": {
            "continent": "America",
            "population": 300000000
        },
        "Israel": {
            "continent": "Asia",
            "population": 3000000
        },
        "Spain": {
            "continent": "Europe",
            "population": 90000000
        }
    }
    countriesDict = json.dumps(j)
    server.wfile.write(bytes(countriesDict, encoding))

def get_variables(server: SimpleHTTPRequestHandler, path: str):
    j = {
        "dynamic_variables": ["total_deaths", "new_deaths", "total_cases", "new_cases", "stringency"],
        "static_variables": ["population", "gdp"]
    }
    variableDict = json.dumps(j)
    server.wfile.write(bytes(variableDict, encoding))

def get_dates(server: SimpleHTTPRequestHandler, path: str):
    j = {
        "first_date": "2020-3-1",
        "last_date": "2020-3-3"
    }
    datesDict = json.dumps(j)
    server.wfile.write(bytes(datesDict, encoding))

def get_map_variable(server: SimpleHTTPRequestHandler, path: str):
    j = {
        "total_deaths": 1000,
        "total_cases": 5000,
        "new_deaths": 10,
        "new_cases": 50,
    }
    dict = json.dumps(j)
    server.wfile.write(bytes(dict, encoding))

def get_data_for_scatter_line_graph(server: SimpleHTTPRequestHandler, path: str):
    if path[-2] == 'y':
        j = {
            "2020-03-01": 120,
            "2020-03-02": 230,
            "2020-03-03": 20,
        }
    else:
        j = {
            "2020-03-01": 10,
            "2020-03-02": 30,
            "2020-03-03": 60,
        }
    dict = json.dumps(j)
    server.wfile.write(bytes(dict, encoding))

def get_static_data():
    f = 100
    j = {
        "value": f,
    }
    dict = json.dumps(j)
    server.wfile.write(bytes(dict, encoding))

def total_deaths_in_each_continent():
    j = {
        "America": 100,
        "Asia": 100,
        "Europe": 100,
        "Africa": 100,
        "Australia": 100,
    }
    dict = json.dumps(j)
    server.wfile.write(bytes(dict, encoding))

def percentage_cases_out_of_total_population_in_each_continent():
    j = {
        "America": {
            "total_cases": 0,
            "total_population": 0,
            "cases_percentage": 100,
        },
        "Asia": 50,
        "Europe": 20,
        "Africa": 80,
        "Australia": 90,
    }
    dict = json.dumps(j)
    server.wfile.write(bytes(dict, encoding))

def total_deaths_of_top_five_human_development_index():
    j = {
        "United States": {
            "human_development_index": 100,
            "total_deaths": 200,
        },
        "Israel": {
            "human_development_index": 100,
            "total_deaths": 200,
        },
        "Spain": {
            "human_development_index": 100,
            "total_deaths": 200,
        }
    }
    dict = json.dumps(j)
    server.wfile.write(bytes(dict, encoding))






def getColumnData(server: SimpleHTTPRequestHandler, path: str):
    j = {
        "2020-3-1": {
            "United States": 1000,
            "Israel": 700,
            "A": 100,
            "b": 100,
            "h": 100,
            "g": 100,
            "e": 100,
            "m": 100,
            "n": 100,
        },
        "2020-3-2": {
            "United States": 1300,
            "Israel": 200,
            "A": 100,
            "b": 100,
            "h": 100,
            "g": 100,
            "e": 100,
            "m": 100,
            "n": 100,
        },
        "2020-3-3": {
            "United States": 500,
            "Israel": 1200,
            "A": 200,
            "b": 0,
            "h": -100,
            "g": 10,
        }
    }
    dict = json.dumps(j)
    server.wfile.write(bytes(dict, encoding))

def ignore(server: SimpleHTTPRequestHandler, path: str):pass

routes_GET = {
    '/favicon.ico': ignore,
    '/': getIndex,
    '/countries': get_countries,
    '/variables': get_variables,
    '/dates': get_dates,
    '/map': get_map_variable,
    '/graph/line': get_data_for_scatter_line_graph,
    '/graph/column': getColumnData,
}

class Server(SimpleHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        self._set_headers()
        if self.path == '/favicon.ico': return
        if self.path == '/': self.path = '/index.html'
        try :print(f"------\n{self.get_query_params(self.path.split('?')[1])}\n------")
        except: pass
        try:
            routes_GET[self.path.split('?')[0]](self, self.path)
        except:
            with open(self.path[1:], 'rb') as f:
                content = f.read()
                f.close()
            self.wfile.write(content)


    def get_query_params(self, string):
        params = string.split('&')
        pDict = {}
        for p in params:
            if p == '': continue
            pair = p.split('=')
            pDict[pair[0]] = pair[1]
        return pDict


print('Server is running')
httpServer = HTTPServer(('localhost', 8000), Server)
httpServer.serve_forever()
