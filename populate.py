from pinecone import Pinecone
from openai import OpenAI
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from atlas import updateAtlas
import os

if not os.path.exists("keys.json"):
    print("Please create and populate keys.json")
    quit()
with open('keys.json', 'r') as f:
    keys = json.load(f)
if not os.path.exists("vectorsWithMetadata.json"):
    with open("vectorsWithMetadata.json", "w") as f:
        print("Initializing vectorsWithMetadata.json")
        f.write("{}")
with open('vectorsWithMetadata.json') as f:
    data = json.load(f)

MODEL = "text-embedding-3-large"
client = OpenAI(api_key=keys["openai"])

pc = Pinecone(api_key=keys["pinecone"])
index = pc.Index("openai")

URL = "https://xkcd.com/info.0.json"
r = requests.get(URL)
newestID = r.json()["num"]

vectorIDToAdd = index.describe_index_stats().total_vector_count + 1
changedSomething = False

repeatTries = 0
while (vectorIDToAdd <= newestID):
    if vectorIDToAdd == 404:
        vectorIDToAdd += 1
        continue
    res = requests.get(f"https://xkcd.com/{vectorIDToAdd}/info.0.json")
    JSON = json.loads(res.text)

    d1 = datetime(int(JSON["year"]), int(JSON["month"]), int(JSON["day"]))
    d2 = datetime.today()
    daysPassed = abs((d2 - d1).days)
    if (daysPassed < 2):
        dayText = "day" if daysPassed == 1 else "days"
        print(f"comic no. {vectorIDToAdd} is only {daysPassed} {dayText} old, minimum 2")
        break
    try:
        URL = f"https://www.explainxkcd.com/wiki/index.php/{vectorIDToAdd}"
        r = requests.get(URL)
        soup = BeautifulSoup(r.text, 'html.parser')

        title = "Title: " + JSON["title"]
        titleText = "Title text: " + JSON["alt"]

        text = title

        transcript = soup.find(id="Transcript")
        if (transcript):
            currentSibling = transcript.parent.findNext("dl")
            text += "\n" + "Transcript: "
            if (currentSibling):
                text += currentSibling.get_text()
                while (currentSibling.name == "dl"):
                    text += "\n" + currentSibling.get_text()
                    currentSibling = currentSibling.next_sibling
        text += "\n" + titleText
        text += "\nExplanation: "
        explanation = soup.select_one("#Explanation, #Explanations, #Brief_Explanation, #Eggsplanation")
        currentSibling = explanation.parent.findNext("p")
        while (currentSibling and str(currentSibling.name).find("h") == -1):
            text += "\n" + currentSibling.get_text()
            currentSibling = currentSibling.next_sibling
        text = text[:1000]
        print(text)
        repeatTries = 0
    except AttributeError:
        if (repeatTries < 3):
            repeatTries += 1
            print("Failed to parse page, retrying...")
            continue
        else:
            raise Exception("Failed to parse page")
    res = client.embeddings.create(
    input=text, model=MODEL
    )
    embed = res.data[0].embedding
    index.upsert(vectors=[
        {"id":str(vectorIDToAdd), "values":embed}
    ])
    changedSomething = True

    data[str(vectorIDToAdd)] = {"id":str(vectorIDToAdd), "values":embed, "title":JSON["title"], "date":(JSON["day"] + "/" + JSON["month"] + "/" + JSON["year"])}

    with open('vectorsWithMetadata.json', 'w') as file:
        file.write(json.dumps(data))
    vectorIDToAdd += 1
print(f"most recently cached is no. {index.describe_index_stats().total_vector_count}")
if (changedSomething):
    updateAtlas()