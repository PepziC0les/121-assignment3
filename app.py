from flask import Flask
from flask import request
from flask import render_template
import json
app = Flask(__name__)

@app.route("/")
def hello():
    return "Welcome to Python Flask!"

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/search", methods=['POST', 'GET'])
def doSearchPost():
    query = request.form['search-query']
    return json.dumps({'status':'OK', 'query':query})

if __name__ == "__main__":
    app.run()