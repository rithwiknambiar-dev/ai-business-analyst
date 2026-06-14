from app.utils.data_manager import DataManager

from src.rag.embedding_generator import (
    EmbeddingGenerator
)

from src.rag.vector_store import (
    VectorStore
)

from src.rag.retriever import (
    Retriever
)


class RAGEngine:

    def __init__(self, df):

        self.df = df

        self.embedding_generator = (
            EmbeddingGenerator()
        )

        dataset_fingerprint = (
            DataManager.get_dataset_fingerprint()
        )

        if not dataset_fingerprint:

            dataset_fingerprint = (
                DataManager.generate_dataset_fingerprint(
                    df
                )
            )

        self.vector_store = (
            VectorStore(
                dataset_fingerprint
            )
        )

        self.retriever = None

        loaded = (
            self.vector_store.load_index()
        )

        if loaded:

            print(
                f"Loaded FAISS index for dataset: "
                f"{dataset_fingerprint[:12]}"
            )

            self.retriever = Retriever(
                self.embedding_generator,
                self.vector_store
            )

        else:

            print(
                "No existing FAISS index found."
            )

            self.build_index()

    def build_index(self):

        print(
            "Building universal dataset documents..."
        )

        documents = []

        max_rows = min(
            len(self.df),
            5000
        )

        for _, row in (
            self.df.head(max_rows)
            .iterrows()
        ):

            row_document = []

            for column in self.df.columns:

                value = row.get(
                    column,
                    ""
                )

                if str(value) == "nan":

                    value = ""

                row_document.append(
                    f"{column}: {value}"
                )

            documents.append(
                "\n".join(
                    row_document
                )
            )

        print(
            f"Generated {len(documents)} documents"
        )

        print(
            "Generating embeddings..."
        )

        embeddings = (
            self.embedding_generator
            .generate_embeddings(
                documents
            )
        )

        print(
            "Embeddings generated"
        )

        self.vector_store.create_index(
            embeddings,
            documents
        )

        print(
            "Saving dataset-specific FAISS index..."
        )

        self.vector_store.save_index()

        self.retriever = Retriever(
            self.embedding_generator,
            self.vector_store
        )

        print(
            "Dataset index ready"
        )

    def retrieve(
        self,
        question
    ):

        if self.retriever is None:

            return []

        return self.retriever.retrieve(
            question,
            top_k=25
        )