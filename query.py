from pinecone import Pinecone
from openai import OpenAI
import json

with open('keys.json', 'r') as f:
    keys = json.load(f)

MODEL = "text-embedding-3-large"
client = OpenAI(api_key=keys["openai"])

pc = Pinecone(api_key=keys["pinecone"])
index = pc.Index("openai")

def query(text):
  res = client.embeddings.create(
    input=text, model=MODEL
    )
  embed = res.data[0].embedding

  queryRes = index.query(
    vector=embed,
    top_k=30,
    include_values=False
  )

  return queryRes.to_dict()