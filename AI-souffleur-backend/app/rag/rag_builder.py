from app.rag.chain import RAGChain
from app.rag.retriever import RAGRetriever
from app.config.config import KRB_COLLECTION_NAME, MMB_COLLECTION_NAME, OPENAI_API_KEY, OPENAI_MODEL_NAME

from langchain_openai import ChatOpenAI 


def create_rag_chain():

    llm_client = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model=OPENAI_MODEL_NAME,
        temperature=0.1,
        streaming=False
    )

    krb_retriever = RAGRetriever(KRB_COLLECTION_NAME)
    mmb_retriever = RAGRetriever(MMB_COLLECTION_NAME)

    rag_chain = RAGChain(
        llm_client=llm_client,
        krb_retriever=krb_retriever,
        mmb_retriever=mmb_retriever
    )

    return rag_chain