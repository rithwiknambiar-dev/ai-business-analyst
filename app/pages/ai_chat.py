import sys
from pathlib import Path

import streamlit as st

project_root = (
    Path(__file__)
    .resolve()
    .parent
    .parent
    .parent
)

sys.path.append(str(project_root))

from app.utils.data_manager import DataManager
from src.ingestion.data_loader import DataLoader
from src.rag.llm_handler import LLMHandler
from src.rag.rag_engine import RAGEngine


# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="AI Business Analyst",
    layout="wide"
)

st.title("AI Business Analyst Chat")

st.markdown(
    """
Ask questions about your dataset.

Examples:

- Which region performs best?
- Which products generate highest profit?
- Which category has highest sales?
- Give me business recommendations.
"""
)

# =====================================
# LOAD DATA
# =====================================

df = DataManager.get_data()

if df is None:
    df = DataLoader.load_data()

# =====================================
# CACHE RAG ENGINE
# =====================================

@st.cache_resource
def load_rag_engine():

    return RAGEngine(df)


with st.spinner(
    "Building RAG Index (First Run Only)..."
):

    rag_engine = load_rag_engine()

llm = LLMHandler()

# =====================================
# CHAT HISTORY
# =====================================

if "messages" not in st.session_state:

    st.session_state.messages = []

# =====================================
# DISPLAY HISTORY
# =====================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

# =====================================
# USER INPUT
# =====================================

question = st.chat_input(
    "Ask a question about the dataset..."
)

if question:

    # User Message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message(
        "user"
    ):

        st.markdown(
            question
        )

    # Assistant Message

    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "Searching Dataset..."
        ):

            retrieved_docs = (
                rag_engine.retrieve(
                    question
                )
            )

            response = (
                llm.ask_rag_question(
                    retrieved_docs,
                    question
                )
            )

            st.markdown(
                response
            )

            with st.expander(
                "View Retrieved Records"
            ):

                for i, doc in enumerate(
                    retrieved_docs,
                    start=1
                ):

                    st.markdown(
                        f"### Record {i}"
                    )

                    st.text(doc)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )