import faiss
import pickle
import numpy as np
from pathlib import Path


class VectorStore:

    def __init__(self):

        self.index = None
        self.documents = []

        self.index_path = (
            Path("data/embeddings/faiss.index")
        )

        self.documents_path = (
            Path("data/embeddings/documents.pkl")
        )

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

    def save_index(self):

        self.index_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        faiss.write_index(
            self.index,
            str(self.index_path)
        )

        with open(
            self.documents_path,
            "wb"
        ) as file:

            pickle.dump(
                self.documents,
                file
            )

    def load_index(self):

        if (
            self.index_path.exists()
            and
            self.documents_path.exists()
        ):

            self.index = faiss.read_index(
                str(self.index_path)
            )

            with open(
                self.documents_path,
                "rb"
            ) as file:

                self.documents = (
                    pickle.load(file)
                )

            return True

        return False

    def search(
        self,
        query_embedding,
        top_k=25
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