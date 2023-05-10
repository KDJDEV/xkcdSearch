from nomic import atlas
import json
import numpy as np

def updateAtlas():
    with open('vectorsWithMetadata.json') as f:
        data = json.load(f)
    embeddings = np.array([data[key]['values'] for key in data])

    project = atlas.map_embeddings(embeddings=embeddings, data=([{"title" : data[key]["title"],"url": "https://xkcd.com/" + data[key]["id"], "date" : data[key]["date"]} for key in data]), name="xkcd", reset_project_if_exists=True)
    projectID = project.id
    mapID = project.get_map(name="xkcd").id
    mapURL = f"https://atlas.nomic.ai/map/preview/{projectID}/{mapID}"
    with open("data/mapURL.txt", "w") as f:
        f.write(mapURL)
    print("updated map")