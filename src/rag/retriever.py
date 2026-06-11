from src.rag.embedding_generator import EmbeddingGenerator
from src.rag.vector_store import InMemoryVectorStore

class RAGRetriever:
    """
    Coordinates query embedding and vector search to retrieve relevant text contexts.
    """
    def __init__(self, vector_store: InMemoryVectorStore, embedding_generator: EmbeddingGenerator):
        self.vector_store = vector_store
        self.embedding_generator = embedding_generator
        
    def retrieve(self, query: str, k=3) -> list[dict]:
        """
        Convert query to vector and find the top k matching chunks.
        """
        if not query.strip():
            return []
            
        # If generator is TF-IDF, it needs to transform the query string
        # using the vocabulary it learned from the document library
        query_vector = self.embedding_generator.get_embeddings([query])[0]
        
        return self.vector_store.similarity_search(query_vector, k=k)
