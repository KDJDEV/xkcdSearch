import pinecone
import openai
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

with open('keys.json', 'r') as f:
    keys = json.load(f)
with open('vectorsWithMetadata.json') as f:
    data = json.load(f)
# initialize connection to pinecone (get API key at app.pinecone.io)
pinecone.init(
    api_key=keys["pinecone"],
    environment="us-west1-gcp-free"  # find next to API key in console
)
index = pinecone.Index('openai')

MODEL = "text-embedding-ada-002"
openai.api_key = keys["openai"]

URL = "https://xkcd.com/info.0.json"
r = requests.get(URL)
newestID = r.json()["num"]

vectorIDToAdd = index.describe_index_stats().total_vector_count + 1
while (vectorIDToAdd <= newestID):

    res = requests.get(f"https://xkcd.com/{vectorIDToAdd}/info.0.json")
    JSON = json.loads(res.text)

    d1 = datetime(int(JSON["year"]), int(JSON["month"]), int(JSON["day"]))
    d2 = datetime.today()
    daysPassed = abs((d2 - d1).days)
    if (daysPassed < 2):
        dayText = "day" if daysPassed == 1 else "days"
        print(f"comic no. {vectorIDToAdd} is only {daysPassed} {dayText} old, minimum 2")
        break
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
    res = openai.Embedding.create(
    input=text, engine=MODEL
    )
    embed = res.data[0].embedding
    index.upsert([
        (str(vectorIDToAdd), embed)
    ])

    data[str(vectorIDToAdd)] = {"id":str(vectorIDToAdd), "values":embed, "title":JSON["title"], "date":(JSON["day"] + "/" + JSON["month"] + "/" + JSON["year"])}

    with open('vectorsWithMetadata.json', 'w') as file:
        file.write(json.dumps(data))
    vectorIDToAdd += 1
print(f"most recently cached is no. {index.describe_index_stats().total_vector_count}")
