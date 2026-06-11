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

from src.rag.rag_engine import (
    RAGEngine
)

from src.rag.llm_handler import (
    LLMHandler
)


df = DataLoader.load_data()

rag = RAGEngine(df)

llm = LLMHandler()

question = (
    "Which technology products are generating the highest profit?"
)

docs = rag.retrieve(
    question
)

response = llm.ask_rag_question(
    docs,
    question
)

print(response)