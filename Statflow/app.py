from flask import Flask
from flask import render_template, session, url_for, redirect, g, request, jsonify, abort
import requests, bcrypt
import json
from flask_pymongo import PyMongo
#import urllib2
from pprint import pprint
import pytemperature
# Pip install pymongo on your machine before running app

# Pass in __name__ to help flask determine root path
app = Flask(__name__) # create the application instance

app.config['MONGO_DBNAME'] = 'weather'
app.config['MONGO_URI'] = 'mongodb://statflow:statflow18@ds113738.mlab.com:13738/weather'

mongo = PyMongo(app)

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
    if 'username' in session:
        userid = session['username']
        return render_template("index.html", user=userid)
        print('you are logged in as ' + session['username'])
        
    else:
        return render_template("login.html") 
        
    

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            #hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            #password = request.form['pass']
            users.insert({'name' : request.form['username'], 'password' : request.form['pass']})
            session['username'] = request.form['username']
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        users = mongo.db.users
        login_user = users.find_one({'name' : request.form['username']})

        if login_user:
            if request.form['pass'] == login_user['password']:
                session['username'] = request.form['username']
                return redirect(url_for('main'))
            else:
                return 'wrong password'
    return render_template('login.html')

"""
    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('main'))
    return 'Invalid username/password combination'
"""

@app.route("/logout")
def logout():
    # remove the username from the session if it is here
    session.pop('username', None)
    return redirect(url_for('main'))

@app.route('/HistoricData', methods=['GET', 'POST'])
def get_HistoricData():
    selection = (r.table('rainfall1').run(g.rdb_conn))

    if request.method == 'POST':
        text1 = request.form['year']
        year = int(str(text1)) # convert to string and then int for year query
        s = (r.table('rainfall1').filter({'Year': year}).run(g.rdb_conn))
        return render_template("HistoricData.html", s=s, selection=selection)
    
    return render_template("HistoricData1.html", selection=selection)


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
            text = request.form['city'] #take input submitted 
            cityname = str(text) #parse the text to a city name
    
            #make a call to the api using the cuty name from dropdown in the request
            re = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+cityname+'&appid=9af800562857988900fdbb172d8962c7')
    
            json_object = re.json() ## returns the json encoded value
            #pprint(json_object) ## simple check to see the data
    
    		# assign variables from json objects needed below for returning to the html page for chart rendering 
            pressure = str(json_object['main']['pressure']) 
            temp_c = pytemperature.k2c((json_object['main']['temp'])) # Kelvin to Celsius
            temp_min = pytemperature.k2c((json_object['main']['temp_min']))#kelvin to celius
            temp_max = pytemperature.k2c((json_object['main']['temp_max']))# kelvin to celius
            humidity = str(json_object['main']['humidity'])
            windspeed = str(3.6 * (json_object['wind']['speed']))# converts from mps to kmh 
           
			# description = str(json_object['weather'][0]['description'])
                       
            
            return render_template('temp.html', cityname=cityname, pressure=pressure, temp=temp_c, temp_min=temp_min, 
                                                temp_max=temp_max, humidity=humidity, selection=selection, windspeed=windspeed)
        
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
    app.secret_key = 'mysecret'
    app.run(debug=True) # Start the web app. debug=True means to auto refresh page after code changes 

