import faiss
import pickle
import numpy as np

from pathlib import Path


class VectorStore:

    def __init__(
        self,
        dataset_fingerprint
    ):

        self.index = None
        self.documents = []

        self.dataset_fingerprint = (
            dataset_fingerprint
        )

        self.base_path = (
            Path("data/embeddings")
            / dataset_fingerprint
        )

        self.index_path = (
            self.base_path
            / "faiss.index"
        )

        self.documents_path = (
            self.base_path
            / "documents.pkl"
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

        self.base_path.mkdir(
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

        if self.index is None:

            return []

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

            if (
                idx >= 0
                and
                idx < len(
                    self.documents
                )
            ):

                results.append(
                    self.documents[idx]
                )

        return results