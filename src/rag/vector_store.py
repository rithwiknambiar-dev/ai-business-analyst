import faiss
import numpy as np


class VectorStore:

    def __init__(self):

        self.index = None
        self.documents = []

    def create_index(
        self,
        embeddings,
        documents
    ):

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(
            dimension
        )

        self.index.add(
            embeddings.astype(
                np.float32
            )
        )

        self.documents = documents

    def search(
        self,
        query_embedding,
        top_k=5
    ):

        distances, indices = (
            self.index.search(
                query_embedding.astype(
                    np.float32
                ),
                top_k
            )
        )

        results = []

        for idx in indices[0]:

            if idx < len(
                self.documents
            ):

                results.append(
                    self.documents[idx]
                )

        return results