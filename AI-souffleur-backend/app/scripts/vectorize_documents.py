import os
from app.config import config
from app.db.vector_store import get_vector_store, purge_vector_store_for_collection

from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def vectorize_knowledge_base(path, collection_name, text_splitter):

    print(f"\n Vectorizing KB: {collection_name} ---")
    print(f"KB path: {path}")

    if not os.path.exists(path):
        print(f"WARN: Path does not exist, skipping: {path}")
        return

    loader = DirectoryLoader(path, glob="**/*.*", show_progress=True, use_multithreading=True)
    documents = loader.load()

    if not documents:
        print(f"No documents found in path {path}. Skipping.")
        return

    print(f"Loaded {len(documents)} documents.")

    splits = text_splitter.split_documents(documents)
    print(f"Split into {len(splits)} chunks.")

    print("Adding custom metadata to chunks...")
    for i, chunk in enumerate(splits):

        source_path = chunk.metadata.get('source', 'Unknown')

        filename = os.path.basename(source_path)

        chunk.metadata['filename'] = filename
        chunk.metadata['chunk_number'] = i+1

    print(f"Embedding and storing chunks in collection: '{collection_name}'...")

    vector_store = get_vector_store(collection_name)
    vector_store.add_documents(splits)

    print(f"Successfully vectorized collection: '{collection_name}'")

if __name__ == "__main__":

    print("Refreshing the vector db")

    purge_vector_store_for_collection(config.KRB_COLLECTION_NAME)
    purge_vector_store_for_collection(config.MMB_COLLECTION_NAME)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=50)

    print("Vectorizing KRB knowledge base")
    vectorize_knowledge_base(
        path=config.KRB_KB_PATH,
        collection_name=config.KRB_COLLECTION_NAME,
        text_splitter=text_splitter
    )

    vectorize_knowledge_base(
        path=config.MMB_KB_PATH,
        collection_name=config.MMB_COLLECTION_NAME,
        text_splitter=text_splitter
    )