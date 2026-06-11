import sys
from pathlib import Path

project_root = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)

sys.path.append(
    str(project_root)
)

from src.ingestion.data_loader import (
    DataLoader
)

from src.rag.embedding_generator import (
    EmbeddingGenerator
)

from src.rag.vector_store import (
    VectorStore
)

from src.rag.retriever import (
    Retriever
)


df = DataLoader.load_data()

documents = []

for _, row in df.iterrows():

    doc = (
        f"Region: {row['Region']}, "
        f"Category: {row['Category']}, "
        f"Sales: {row['Sales']}, "
        f"Profit: {row['Profit']}"
    )

    documents.append(doc)

embedding_generator = (
    EmbeddingGenerator()
)

embeddings = (
    embedding_generator
    .generate_embeddings(
        documents
    )
)

vector_store = VectorStore()

vector_store.create_index(
    embeddings,
    documents
)

retriever = Retriever(
    embedding_generator,
    vector_store
)

results = retriever.retrieve(
    "highest profit technology sales"
)

print("\nRAG RESULTS\n")

for result in results:

    print(result)