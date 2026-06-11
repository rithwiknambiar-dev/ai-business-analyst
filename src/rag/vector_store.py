import numpy as np

class InMemoryVectorStore:
    """
    A lightweight, in-memory vector database for storing text chunks and their embeddings.
    """
    def __init__(self):
        self.documents = []  # list of {"text": str, "metadata": dict}
        self.embeddings = []  # list of np.ndarray
        
    def add_documents(self, documents: list[dict], embeddings: list[np.ndarray]):
        """
        Add documents and their matching embeddings to the store.
        """
        assert len(documents) == len(embeddings), "Count of documents must equal count of embeddings."
        for doc, emb in zip(documents, embeddings):
            self.documents.append(doc)
            self.embeddings.append(emb)
            
    def similarity_search(self, query_vector: np.ndarray, k=3) -> list[dict]:
        """
        Find the top k most similar documents to the query vector using Cosine Similarity.
        """
        if not self.embeddings:
            return []
            
        # Ensure query is flat numpy array
        qv = np.array(query_vector).flatten()
        
        scores = []
        for emb, doc in zip(self.embeddings, self.documents):
            ev = np.array(emb).flatten()
            
            # Align dimensionality in case TF-IDF vectors have mismatched sizes
            if len(qv) != len(ev):
                # Standardize sizes by padding/truncating
                max_len = max(len(qv), len(ev))
                qv_padded = np.zeros(max_len)
                ev_padded = np.zeros(max_len)
                qv_padded[:len(qv)] = qv
                ev_padded[:len(ev)] = ev
                
                # Cosine Similarity
                dot_product = np.dot(qv_padded, ev_padded)
                norm_q = np.linalg.norm(qv_padded)
                norm_e = np.linalg.norm(ev_padded)
            else:
                dot_product = np.dot(qv, ev)
                norm_q = np.linalg.norm(qv)
                norm_e = np.linalg.norm(ev)
                
            similarity = dot_product / (norm_q * norm_e) if (norm_q > 0 and norm_e > 0) else 0.0
            scores.append((doc, similarity))
            
        # Sort by similarity descending
        scores.sort(key=lambda x: x[1], reverse=True)
        
        # Return top k documents
        return [doc for doc, score in scores[:k]]
        
    def clear(self):
        """Reset the database."""
        self.documents = []
        self.embeddings = []
ColoredText = str
