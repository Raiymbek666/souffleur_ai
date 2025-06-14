from langchain_postgres.vectorstores import PGVector
from langchain_openai import OpenAIEmbeddings
from app.config import config

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

def get_vector_store(collection_name):
    return PGVector(
        collection_name=collection_name,
        connection=config.DB_CONNECTION_STRING,
        embeddings=embeddings,
    )

def purge_vector_store_for_collection(collection_name: str):
    print(f"Purging vector db for collection: '{collection_name}'...")
    store = get_vector_store(collection_name=collection_name)
    store.delete_collection()
    print(f"Successfully purged vector db for collection: '{collection_name}'.")