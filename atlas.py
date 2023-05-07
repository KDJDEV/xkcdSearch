from nomic import atlas
import json
import numpy as np
import requests

with open('vectorsWithMetadata.json') as f:
    data = json.load(f)
embeddings = np.array([data[key]['values'] for key in data])
"""
with open('vectors.json') as f:
    data = json.load(f)
for key in data:
    datum = data[key]
    id = datum["id"]
    if (id == "404"):
        datum["title"] = "Not Found"
        datum["date"] = "1/4/2008"
    else:
        URL = f"https://xkcd.com/{id}/info.0.json"
        r = requests.get(URL)
        JSON = r.json()
        datum["title"] = JSON["title"]
        datum["date"] = JSON["day"] + "/" + JSON["month"] + "/" + JSON["year"]
    print(id)
with open('vectorsWithMetadata.json', 'w') as file:
    file.write(json.dumps(data))
"""

project = atlas.map_embeddings(embeddings=embeddings, data=([{"title" : data[key]["title"],"url": "https://xkcd.com/" + data[key]["id"], "date" : data[key]["date"]} for key in data]), name="xkcd", reset_project_if_exists=True)
projectID = project.id
mapID = project.get_map(name="xkcd").id
mapURL = f"https://atlas.nomic.ai/map/preview/{projectID}/{mapID}"
with open("data/mapURL.txt", "w") as f:
    f.write(mapURL)
print("updated map")