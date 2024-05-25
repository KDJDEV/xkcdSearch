from nomic import atlas
import json
import numpy as np
from sklearn.decomposition import PCA

def updateAtlas():
    with open('vectorsWithMetadata.json') as f:
        data = json.load(f)
    embeddings = np.array([data[key]['values'] for key in data])
    
    pca = PCA(n_components=2048)
    reduced_embeddings = pca.fit_transform(embeddings)
    project = atlas.map_data(embeddings=reduced_embeddings, data=([{"title" : data[key]["title"],"url": "https://xkcd.com/" + data[key]["id"], "date" : data[key]["date"]} for key in data]), identifier="xkcd")
    projectID = project.id
    mapID = project.get_map(name="xkcd").id
    mapURL = f"https://atlas.nomic.ai/map/{projectID}/{mapID}"
    with open("data/mapURL.txt", "w") as f:
        f.write(mapURL)
    print("updated map")