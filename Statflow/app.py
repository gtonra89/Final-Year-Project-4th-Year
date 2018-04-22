from flask import Flask #Importing flask app

from flask import render_template, flash, session, url_for, redirect, g, request, jsonify, abort

import requests, json

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
 

# Using werkzeug library to encrypt user passwords
from werkzeug.security import generate_password_hash, check_password_hash 

# PyMongo allows us to work directly with the mongo database without defining a schema. It is a wrapper for mongodb library in flask
from flask_pymongo import PyMongo  

import pytemperature
import time
import re as res

# Pip install pymongo on your machine before running app
# Pass in __name__ to help flask determine root path
app = Flask(__name__) # create the application instance

# Configurating our database with flask
app.config['MONGO_DBNAME'] = 'weather' # 'weather' is our db name on mlab
# URI (Uniform Resource Locator) is supplied by mlab. This identifies and locates where the database is on mlab
app.config['MONGO_URI'] = 'mongodb://statflow:statflow18@ds113738.mlab.com:13738/weather'

mongo = PyMongo(app) # Initialise connection to mongo database.

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
    # if username is logged in
    if 'username' in session:
        # flash a message to user to indicate they are logged in.
        flash("Logged in as " + session['username'])
        return render_template("index.html")
    else:
        return render_template("login.html") 
        
# Registration
@app.route('/register', methods=['POST', 'GET'])
def register():
    error = None
    if request.method == 'POST':
        users = mongo.db.users # Accessing our users collections
        # Checking to see if a username already exist in the users collection
        existing_user = users.find_one({'name' : request.form['username']})

        # if theres no existing username
        if existing_user is None:
            # Generating sha256 hash from user password
            hashpass = generate_password_hash(request.form['pass'], method='sha256')
            # Add new user to users collection along with password
            users.insert({'name' : request.form['username'], 'password' : hashpass})
            # Activate a session using that username
            #session['username'] = request.form['username']
        # Once user is registered.. return login page for them to login
            return redirect(url_for('login'))
        else:
            error = 'Username already exists'
            #return redirect(url_for('register'))
            
        
    return render_template('register.html', error=error)

# Login
@app.route('/login', methods=['GET','POST'])
def login():
    error = None # error variable set to None as default.
    if request.method == 'POST':
        users = mongo.db.users # access the users collection in the database
        # Checking to see if username exists
        login_user = users.find_one({'name' : request.form['username']})

        if login_user: # if it does exist
            # check to see if password hash is equal to password hash in the database
            if check_password_hash(login_user['password'], request.form['pass']):
                # if password is correct then activate user session using the username
                session['username'] = request.form['username']
                return redirect(url_for('main')) # redirect to main route
            # if password does not match then...
            else: 
                # error takes in a string message
                error = 'Incorrect username/password'
                #return 'wrong password' # Login failed
        else:
            error = 'Incorrect username/password'
    # return login page and also pass in error message
    return render_template('login.html', error=error)

# Login
@app.route("/logout")
def logout():
    # remove the username from the session if logout button is pressed
    session.pop('username', None)
    # Flash a message to user to indicate they are logged out
    flash("You are now logged out")
    return redirect(url_for('main')) # redirect to main route

@app.route('/HistoricData', methods=['GET', 'POST'])
def get_HistoricData():
    selection = (r.table('rainfall1').run(g.rdb_conn))

    if request.method == 'POST':
        text1 = request.form['year']
        year = int(str(text1)) # convert to string and then int for year query
        s = (r.table('rainfall1').filter({'Year': year}).run(g.rdb_conn))
        return render_template("HistoricData.html", s=s, selection=selection, year=year)
    
    return render_template("HistoricData1.html", selection=selection)

@app.route('/services') #connect a webpage. '/' is a root directory.
def services():
    return render_template("services.html")

@app.route('/team') #connect a webpage. '/' is a root directory.
def team():
    return render_template("team.html")

@app.route('/contact', methods=['GET', 'POST']) #connect a webpage. '/' is a root directory.
def contact():
   
    if request.method == 'POST':
        fromaddr = request.form['email']
        print(fromaddr)
        text1 = request.form['message']
        toaddr = "statflow18@gmail.com"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "INFO"
        body = text1
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(toaddr, "Statflow2018")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        flash('Your email was successfully sent')
        return render_template("contact.html")
 
    return render_template("contact.html")


@app.route('/dashboard') #connect a webpage. '/' is a root directory.
def dashboard():
    return render_template("dashboard.html")

@app.route('/map', methods=['GET', 'POST']) #connect a webpage. '/' is a root directory.
def a():
    return render_template("map.html")

@app.route('/machine', methods=['GET', 'POST']) #connect a webpage. '/' is a root directory.
def machine():
    return render_template("machineMenu.html")

@app.route('/athenry', methods=['GET', 'POST']) #connect a webpage. '/' is a root directory.
def athenry():
    return render_template("MLTemplates/Athenry-Dataset.html")


@app.route('/temp', methods=['GET', 'POST'])
def temp():
        #make inital call to db for citylist in the database
        selection = (r.table('citylist').filter({'country': 'IE'}).run(g.rdb_conn))
        
        #when a submit /post method is made on the page fall into the if statement 
        if request.method == 'POST':
            text = request.form['city'] #take input submitted

            #parse the text to a city name
            cityname = str(text) 
    
            #make a call to the api using the cuty name from dropdown in the request
            re = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+cityname+'&appid=9af800562857988900fdbb172d8962c7')

            # returns the json encoded value    
            json_object = re.json() 
            
    
    		# assign variables from json objects needed below for returning to the html page for chart rendering 
            pressure = str(json_object['main']['pressure']) 
            temp_c = pytemperature.k2c((json_object['main']['temp'])) # Kelvin to Celsius
            temp_min = pytemperature.k2c((json_object['main']['temp_min']))#kelvin to celius
            temp_max = pytemperature.k2c((json_object['main']['temp_max']))# kelvin to celius
            humidity = str(json_object['main']['humidity'])
            windspeed = str(3.6 * (json_object['wind']['speed']))# converts from mps to kmh 
           
			
                       
            #pass back the data to the html page 
            return render_template('temp.html', cityname=cityname, pressure=pressure, temp=temp_c, temp_min=temp_min, 
                                                temp_max=temp_max, humidity=humidity, selection=selection, windspeed=windspeed)
        
        return render_template('temp1.html', selection=selection)

@app.route('/fiveday', methods=['GET', 'POST'])
def fiveday():
    #make inital call to db for citylist in the database
    selectionB = (r.table('citylist').filter({'country': 'IE'}).distinct().run(g.rdb_conn))
    
    #when a submit /post method is made on the page fall into the if statement    
    if request.method == 'POST':
        text = request.form['cityID'] #take input submitted
        cityname = str(text) #parse the text to a city name
        
        #find the corrosponding city id by filtering
        selection1 = (r.table("citylist").filter({"name": cityname}).order_by(r.desc("name")).pluck("id").run(g.rdb_conn))          
        
        #parse the data from database to string
        s1 = str(selection1)
        
        # get rid of any non numeric chars
        result = res.sub('[^0-9]','', s1)
        
        #make call to the api to get the 5 day forcast details       
        re = requests.get('http://api.openweathermap.org/data/2.5/forecast?id='+result+'&appid=9af800562857988900fdbb172d8962c7')
        
        #convert to json notation        
        json_object = re.json()
        
        #pass back the data to the html page 
        return render_template('fiveday.html', json_object=json_object, selectionB=selectionB, cityname=cityname)

    return render_template('fiveday1.html', selectionB=selectionB)



# only run the app whenever this file is called directly..
# for more: https://stackoverflow.com/questions/419163/what-does-if-name-main-do
if __name__ == "__main__":
    # In order to use sessions you have to set a secret key for encryption purposes as a user could hack into the contents of a cookie and modify if there was no secret key used for signing the cookies.
    app.secret_key = 'mysecret' 
    app.run(debug=True, threaded=True) # Start the web app. debug=True means to auto refresh page after code changes instead of having to run the file after every change. 

