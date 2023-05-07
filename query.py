import pinecone
import openai
import json

with open('keys.json', 'r') as f:
    keys = json.load(f)

pinecone.init(
    api_key=keys["pinecone"],
    environment="us-west1-gcp-free"  # find next to API key in console
)
index = pinecone.Index('openai')

MODEL = "text-embedding-ada-002"
openai.api_key = keys["openai"]

def query(text):
  res = openai.Embedding.create(input=text, engine=MODEL)
  embed = res.data[0].embedding

  queryRes = index.query(
    vector=embed,
    top_k=30,
    include_values=False
  )

  return queryRes.to_dict()