import os
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Qdrant

QDRANT_PATH = os.getenv("QDRANT_PATH", "./qdrant_data")
COLLECTION = os.getenv("QDRANT_COLLECTION", "pdf_chunks")

def get_embeddings():
# OpenAI's compact model is fine for demo
return OpenAIEmbeddings(model="text-embedding-3-small")

def get_qdrant_client():
# Local, file-based Qdrant (no external service needed)
os.makedirs(QDRANT_PATH, exist_ok=True)
return QdrantClient(path=QDRANT_PATH)

def get_vectorstore():
client = get_qdrant_client()
return Qdrant(client=client, collection_name=COLLECTION, embeddings=get_embeddings())