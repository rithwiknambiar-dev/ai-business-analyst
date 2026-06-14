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
from src.rag.llm_handler import LLMHandler
from src.rag.rag_engine import RAGEngine


# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="AI Data Analyst Chat",
    layout="wide"
)

st.title("🤖 AI Data Analyst Chat")

# =====================================
# LOAD DATA
# =====================================

df = DataManager.get_data()

if df is None:

    st.warning(
        "Please upload and select a dataset first."
    )

    st.stop()

# =====================================
# DATASET INFO
# =====================================

dataset_name = (
    DataManager.get_active_dataset_name()
)

dataset_summary = (
    DataManager.get_dataset_summary()
)

dataset_fingerprint = (
    DataManager.get_dataset_fingerprint()
)

if dataset_fingerprint is None:

    st.error(
        "Dataset fingerprint not found."
    )

    st.stop()

# =====================================
# RESET CHAT IF DATASET CHANGES
# =====================================

previous_dataset = (
    st.session_state.get(
        "chat_dataset"
    )
)

if previous_dataset != dataset_fingerprint:

    st.session_state.messages = []

    st.session_state[
        "chat_dataset"
    ] = dataset_fingerprint

# =====================================
# DATASET HEADER
# =====================================

st.success(
    f"Active Dataset: {dataset_name}"
)

if dataset_summary:

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Dataset Type",
            dataset_summary.get(
                "dataset_type",
                "Generic"
            )
        )

    with col2:

        st.metric(
            "Rows",
            dataset_summary.get(
                "row_count",
                0
            )
        )

    with col3:

        st.metric(
            "Columns",
            dataset_summary.get(
                "column_count",
                0
            )
        )

# =====================================
# DYNAMIC QUESTIONS
# =====================================

if dataset_summary:

    st.markdown(
        "### Suggested Questions"
    )

    for question in dataset_summary.get(
        "suggested_questions",
        []
    ):

        st.info(question)

# =====================================
# RAG LOADER
# =====================================

@st.cache_resource
def load_rag_engine(
    fingerprint,
    dataframe
):

    return RAGEngine(
        dataframe
    )

with st.spinner(

    "Preparing your dataset for AI search..."
):

    rag_engine = load_rag_engine(
        dataset_fingerprint,
        df
    )

# =====================================
# LLM
# =====================================

llm = LLMHandler()

# =====================================
# CHAT HISTORY
# =====================================

if "messages" not in st.session_state:

    st.session_state.messages = []

# =====================================
# DISPLAY CHAT
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
    "Ask anything about your dataset..."
)

if question:

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

    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "Analyzing dataset..."
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
                "Retrieved Context"
            ):

                for i, doc in enumerate(
                    retrieved_docs,
                    start=1
                ):

                    st.markdown(
                        f"### Document {i}"
                    )

                    st.text(doc)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )