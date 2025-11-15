from typing import List
import nltk
from sentence_transformers import SentenceTransformer

# download punkt once (Dockerfile also downloads)
nltk.download("punkt", quiet=True)

# load embedding model globally
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
_embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Returns embeddings as plain Python lists.
    """
    arr = _embedding_model.encode(texts, convert_to_numpy=False)
    # ensure lists (some frameworks return lists anyway)
    return [list(x) for x in arr]
