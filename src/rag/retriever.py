class Retriever:

    def __init__(
        self,
        embedding_generator,
        vector_store
    ):

        self.embedding_generator = (
            embedding_generator
        )

        self.vector_store = (
            vector_store
        )

    def retrieve(
        self,
        query,
        top_k=10
    ):

        query_embedding = (
            self.embedding_generator
            .generate_embeddings(
                [query]
            )
        )

        results = (
            self.vector_store
            .search(
                query_embedding,
                top_k
            )
        )

        return results