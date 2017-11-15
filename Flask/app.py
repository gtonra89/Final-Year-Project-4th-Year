from flask import Flask, render_template 

# Pass in __name__ to help flask determine root path
app = Flask(__name__) # create the application instance

# Routing/Mapping
# @ signifies a decorator which is a way to wrap a function and modify its behaviour
@app.route('/') #connect a webpage. '/' is a root directory.
def main():
    return render_template("index.html")


if __name__ == "__main__":
    app.run() # Start the web app