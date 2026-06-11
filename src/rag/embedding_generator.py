import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import google.generativeai as genai
import openai
from src.utils.config import GEMINI_API_KEY, OPENAI_API_KEY

class EmbeddingGenerator:
    """
    Generate embeddings for text chunks.
    Supports API models (Gemini/OpenAI) and falls back to TF-IDF representations.
    """
    def __init__(self, use_provider="tfidf", api_key=None):
        self.provider = use_provider.lower()
        self.api_key = api_key
        self.vectorizer = None
        
        # Configure APIs if keys provided
        if self.provider == "gemini" and (self.api_key or GEMINI_API_KEY):
            genai.configure(api_key=self.api_key or GEMINI_API_KEY)
        elif self.provider == "openai" and (self.api_key or OPENAI_API_KEY):
            openai.api_key = self.api_key or OPENAI_API_KEY
            
    def get_embeddings(self, texts: list[str]) -> list[np.ndarray]:
        """
        Convert a list of strings into a list of vector representations.
        """
        if not texts:
            return []
            
        if self.provider == "gemini":
            try:
                embeddings = []
                for text in texts:
                    response = genai.embed_content(
                        model="models/embedding-001",
                        content=text,
                        task_type="retrieval_document"
                    )
                    embeddings.append(np.array(response['embedding']))
                return embeddings
            except Exception as e:
                # Fall back to TF-IDF on failure
                self.provider = "tfidf"
                
        if self.provider == "openai":
            try:
                client = openai.OpenAI(api_key=self.api_key or OPENAI_API_KEY)
                response = client.embeddings.create(
                    model="text-embedding-ada-002",
                    input=texts
                )
                return [np.array(emb.embedding) for emb in response.data]
            except Exception as e:
                # Fall back to TF-IDF on failure
                self.provider = "tfidf"
                
        # TF-IDF Fallback
        if self.provider == "tfidf":
            if not self.vectorizer:
                # Fit vectorizer on current texts
                self.vectorizer = TfidfVectorizer(stop_words='english', min_df=1)
                vectors = self.vectorizer.fit_transform(texts).toarray()
            else:
                # Fit already happened, transform
                try:
                    vectors = self.vectorizer.transform(texts).toarray()
                except Exception:
                    # Re-fit in case vocabulary changes
                    self.vectorizer = TfidfVectorizer(stop_words='english', min_df=1)
                    vectors = self.vectorizer.fit_transform(texts).toarray()
            return [np.array(vec) for vec in vectors]
            
        return [np.zeros(128) for _ in texts]
