from typing import List
import os
from dotenv import load_dotenv
load_dotenv()



from pinecone import Pinecone, ServerlessSpec

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# If you need to create an index:
if "my-index" not in [i.name for i in pc.list_indexes()]:
    pc.create_index(
        name="my-index",
        dimension=768,  # match your embedding model
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

index = pc.Index("my-index")



def query_vectors(embedding, top_k=5):
    # Convert to list
    if hasattr(embedding, "tolist"):
        embedding = embedding.tolist()
    res = index.query(vector=embedding, top_k=top_k, include_metadata=True)
    return res.matches  # <-- return the actual list of matches
