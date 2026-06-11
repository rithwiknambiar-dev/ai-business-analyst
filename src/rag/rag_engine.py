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

        self.vector_store = (
            VectorStore()
        )

        self.retriever = None

        loaded = (
            self.vector_store.load_index()
        )

        if loaded:

            print(
                "Existing FAISS Index Loaded"
            )

            self.retriever = Retriever(
                self.embedding_generator,
                self.vector_store
            )

        else:

            print(
                "No Saved Index Found"
            )

            self.build_index()

    def build_index(self):

        documents = []

        print(
            "Building Documents..."
        )

        for _, row in (
            self.df.head(2000)
            .iterrows()
        ):

            document = f"""
Region: {row.get('Region', '')}
Category: {row.get('Category', '')}
Sub-Category: {row.get('Sub-Category', '')}
Product Name: {row.get('Product Name', '')}
Segment: {row.get('Segment', '')}
Sales: {row.get('Sales', '')}
Profit: {row.get('Profit', '')}
Quantity: {row.get('Quantity', '')}
Discount: {row.get('Discount', '')}
"""

            documents.append(
                document
            )

        print(
            f"Documents: {len(documents)}"
        )

        print(
            "Generating Embeddings..."
        )

        embeddings = (
            self.embedding_generator
            .generate_embeddings(
                documents
            )
        )

        print(
            "Embeddings Generated"
        )

        self.vector_store.create_index(
            embeddings,
            documents
        )

        print(
            "Saving FAISS Index..."
        )

        self.vector_store.save_index()

        print(
            "FAISS Saved"
        )

        self.retriever = Retriever(
            self.embedding_generator,
            self.vector_store
        )

    def retrieve(
        self,
        question
    ):

        return self.retriever.retrieve(
            question,
            top_k=25
        )