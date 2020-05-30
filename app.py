from flask import Flask
from flask import request
from flask import render_template
import json
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("search.html")


@app.route("/search")
def search():
    query = request.args.get("query")
    print(query)
    return {"result":query}

if __name__ == "__main__":
    app.run()