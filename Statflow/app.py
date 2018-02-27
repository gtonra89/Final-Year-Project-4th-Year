from flask import Flask, render_template, request, url_for, redirect, g, request, jsonify, abort
import requests
import json
from flask_pymongo import PyMongo
import urllib2
from pprint import pprint
import pytemperature
# Pip install pymongo on your machine before running app

# Pass in __name__ to help flask determine root path
app = Flask(__name__) # create the application instance

app.config['MONGO_DBNAME'] = 'weather'
app.config['MONGO_URI'] = 'mongodb://statflow:statflow18@ds113738.mlab.com:13738/weather'

#rethink imports
import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError, RqlDriverError

#rethink config
RDB_HOST =  'localhost'
RDB_PORT = 28015
STATFLOW_DB = 'statflow'

# db setup; only run once
def dbSetup():
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    try:
        r.db_create(STATFLOW_DB).run(connection)
        r.db(STATFLOW_DB).table_create('rainfall1').run(connection)
        r.db(STATFLOW_DB).table_create('citylist').run(connection)
        print('Database setup completed')
    except RqlRuntimeError:
        print('Database already exists.')
       
    finally:
        connection.close()
dbSetup()

# open connection before each request
@app.before_request
def before_request():
    try:
        g.rdb_conn = r.connect(host=RDB_HOST, port=RDB_PORT, db=STATFLOW_DB)
    except RqlDriverError:
        abort(503, "Database connection could be established.")

# close the connection after each request
@app.teardown_request
def teardown_request(exception):
    try:
        g.rdb_conn.close()
    except AttributeError:
        pass

# Routing/Mapping
# @ signifies a decorator which is a way to wrap a function and modify its behaviour
@app.route('/') #connect a webpage. '/' is a root directory.
def main():
    
   return render_template("index.html")

@app.route('/HistoricData', methods=['GET'])
def get_HistoricData():
    selection = list(r.table('rainfall1').run(g.rdb_conn)) 
    
    return render_template("HistoricData.html", selection=selection)


@app.route('/Patterns') #connect a webpage. '/' is a root directory.
def Patterns():
    return render_template("Patterns.html")


@app.route('/dashboard') #connect a webpage. '/' is a root directory.
def dashboard():
    return render_template("dashboard.html")

@app.route('/map') #connect a webpage. '/' is a root directory.
def a():
    return render_template("map.html")


@app.route('/temp', methods=['GET', 'POST'])
def temp():
        selection = (r.table('citylist').filter({'country': 'IE'}).run(g.rdb_conn))
        if request.method == 'POST':
            text = request.form['city']
            
            
            cityname = str(text)
            re = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+cityname+'&appid=9af800562857988900fdbb172d8962c7')
            json_object = re.json()
            
            pressure = str(json_object['main']['pressure'])
            temp_c = pytemperature.k2c((json_object['main']['temp'])) # Kelvin to Celsius
            temp_min = pytemperature.k2c((json_object['main']['temp_min']))#kelvin to celius
            temp_max = pytemperature.k2c((json_object['main']['temp_max']))# kelvin to celius
            humidity = str(json_object['main']['humidity'])
            
            
            return render_template('temp.html', cityname=cityname, pressure=pressure, temp=temp_c, temp_min=temp_min, temp_max=temp_max, humidity=humidity, selection=selection)
        
        return render_template('temp1.html', selection=selection)

@app.route('/fiveday')
def fiveday():
    
    r = requests.get('http://api.openweathermap.org/data/2.5/forecast?id=2964179&appid=9af800562857988900fdbb172d8962c7')
    json_object = r.json()
    #for j in json_object["list"]:
     #   print(j["main"]["temp"])

    return render_template('fiveday.html', json_object=json_object)




@app.route('/data')
def data():
    rainfall = mongo.db.rainfall

    result = rainfall.find_one({'name' : 'rainfall'}, {'year': 2017})

    return jsonify({'results' : result['data']})


if __name__ == "__main__":
    app.run(debug=True) # Start the web app. debug=True means to auto refresh page after code changes 

