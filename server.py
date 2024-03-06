from flask import Flask, request, jsonify, Response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import send_from_directory
from query import query
import json
import requests
from pinecone import Pinecone

with open('keys.json', 'r') as f:
    keys = json.load(f)

pc = Pinecone(api_key=keys["pinecone"])

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[],
    storage_uri="memory://",
)

@app.route("/")
def index():
    return send_from_directory("site/dist", "index.html")

@app.route('/<path:path>')
def send_static_files(path):
    return send_from_directory("site/dist", path)

@app.route("/search")
@limiter.limit("50/day;10/minute")
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

@app.route("/getMapURL")
def getMapURL():
    with open("data/mapURL.txt", "r") as f:
        response = Response(f.read(), mimetype="text/plain")
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    
@app.route("/getMostRecentComicID")
def getMostRecentComicID():
    index = pc.Index("openai")
    response = Response(str(index.describe_index_stats().total_vector_count), mimetype="text/plain")
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

if __name__ == '__main__':
   app.run(port=80, debug=False)