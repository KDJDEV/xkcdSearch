from flask import Flask, request, jsonify, Response
from query import query
import json
import requests

app = Flask(__name__)

@app.route("/search")
def search():
    res = query(request.args.get("q"))
    matches = res["matches"]
    response = jsonify(matches)
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route("/fetchxkcd/<int:id>")
def fetchxkcd(id):
    data = requests.get(f"https://xkcd.com/{id}/info.0.json")
    response = Response(data.text, mimetype="text/json")
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


app.run(debug = False)