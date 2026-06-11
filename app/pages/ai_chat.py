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

sys.path.append(
    str(project_root)
)

from app.utils.data_manager import DataManager

from src.ingestion.data_loader import DataLoader

from src.eda.exploratory_analysis import (
    ExploratoryAnalysis
)

from src.insights.insight_generator import (
    InsightGenerator
)

from src.rag.context_builder import (
    ContextBuilder
)

from src.rag.llm_handler import (
    LLMHandler
)


st.set_page_config(
    page_title="AI Business Analyst",
    layout="wide"
)

st.title(
    "AI Business Analyst Chat"
)

# ---------------------------------
# LOAD DATA
# ---------------------------------

df = DataManager.get_data()

if df is None:

    df = DataLoader.load_data()

# ---------------------------------
# GENERATE CONTEXT
# ---------------------------------

eda = ExploratoryAnalysis(df)

eda_report = (
    eda.generate_eda_report()
)

insights = (
    InsightGenerator(
        eda_report
    )
    .generate_all_insights()
)

context = (
    ContextBuilder(
        eda_report,
        insights
    )
    .build_context()
)

llm = LLMHandler()

# ---------------------------------
# CHAT HISTORY
# ---------------------------------

if (
    "messages"
    not in st.session_state
):

    st.session_state.messages = []

# ---------------------------------
# DISPLAY HISTORY
# ---------------------------------

for message in (
    st.session_state.messages
):

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

# ---------------------------------
# USER INPUT
# ---------------------------------

question = st.chat_input(
    "Ask a question about the dataset..."
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

        st.markdown(question)

    with st.chat_message(
        "assistant"
    ):

        with st.spinner(
            "Analyzing..."
        ):

            response = (
                llm.ask_question(
                    context,
                    question
                )
            )

            st.markdown(
                response
            )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )