import pinecone
import openai

pinecone.init(
    api_key="6dfed7eb-243c-44fd-9823-5c9eb398acb8",
    environment="us-west1-gcp-free"  # find next to API key in console
)
index = pinecone.Index('openai')

MODEL = "text-embedding-ada-002"
openai.api_key = "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"

def query(text):
  res = openai.Embedding.create(input=text, engine=MODEL)
  embed = res.data[0].embedding

  queryRes = index.query(
    vector=embed,
    top_k=10,
    include_values=False
  )

  return queryRes.to_dict()