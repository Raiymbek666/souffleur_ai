from app.db.vector_store import get_vector_store
from app.config.config import KRB_COLLECTION_NAME, MMB_COLLECTION_NAME


class RAGRetriever:
    def __init__(self, collection_name):
        self.vector_store = get_vector_store(collection_name)
    def retrieve(self, query, k=3):
        results_with_scores = self.vector_store.similarity_search_with_relevance_scores(query, k)

        relevant_chunks = []
        for chunk, relevance_score in results_with_scores:
            relevant_chunks.append({
                "text": chunk.page_content,
                "filename": chunk.metadata.get("filename", "Unknown"),
                "relevance_score": relevance_score
            }) 
        return relevant_chunks