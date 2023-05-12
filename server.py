from flask import Flask, request, jsonify, Response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import send_from_directory
from query import query
import json
import requests
import pinecone

with open('keys.json', 'r') as f:
    keys = json.load(f)
# initialize connection to pinecone (get API key at app.pinecone.io)
pinecone.init(
    api_key=keys["pinecone"],
    environment="us-west1-gcp-free"  # find next to API key in console
)
index = pinecone.Index('openai')

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
    index = pinecone.Index('openai')
    response = Response(str(index.describe_index_stats().total_vector_count), mimetype="text/plain")
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
app.run()