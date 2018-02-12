from flask import Flask, render_template, request, url_for, redirect, g, request, jsonify, abort
from flask_pymongo import PyMongo
# Pip install pymongo on your machine before running app

# Pass in __name__ to help flask determine root path
app = Flask(__name__) # create the application instance

app.config['MONGO_DBNAME'] = 'weather'
app.config['MONGO_URI'] = 'mongodb://statflow:statflow18@ds113738.mlab.com:13738/weather'

# rethink imports
#import rethinkdb as r
#from rethinkdb.errors import RqlRuntimeError, RqlDriverError

# rethink config
#RDB_HOST =  'localhost'
#RDB_PORT = 28015
#STATFLOW_DB = 'statflow'

# db setup; only run once
"""def dbSetup():
    connection = r.connect(host=RDB_HOST, port=RDB_PORT)
    try:
        r.db_create(STATFLOW_DB).run(connection)
        r.db(STATFLOW_DB).table_create('historic').run(connection)
        print('Database setup completed')
    except RqlRuntimeError:
        print('Database already exists.')
       
    finally:
        connection.close()
dbSetup()
"""
"""
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
"""
# Routing/Mapping
# @ signifies a decorator which is a way to wrap a function and modify its behaviour
@app.route('/') #connect a webpage. '/' is a root directory.
def main():
    
    return render_template("index.html")
"""
@app.route('/HistoricData', methods=['GET'])
def get_HistoricData():
    selection = list(r.table('historic').run(g.rdb_conn)) 
    
    return render_template("HistoricData.html", selection=selection)
"""

@app.route('/Patterns') #connect a webpage. '/' is a root directory.
def Patterns():
    return render_template("Patterns.html")


@app.route('/dashboard') #connect a webpage. '/' is a root directory.
def dashboard():
    return render_template("dashboard.html")

@app.route('/data')
def data():
    rainfall = mongo.db.rainfall

    result = rainfall.find_one({'name' : 'rainfall'}, {'year': 2017})

    return jsonify({'results' : result['data']})


if __name__ == "__main__":
    app.run(debug=True) # Start the web app. debug=True means to auto refresh page after code changes 

