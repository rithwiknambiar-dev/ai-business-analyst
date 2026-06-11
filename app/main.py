import streamlit as st
import pandas as pd
from src.ingestion.data_loader import load_data, validate_dataframe
from src.utils.helpers import inject_premium_css, render_metric_card
from src.utils.config import APP_TITLE
from src.rag.vector_store import InMemoryVectorStore
from src.rag.embedding_generator import EmbeddingGenerator
from src.rag.document_processor import convert_dataframe_to_chunks
import os

# Set page config
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if "df" not in st.session_state:
    st.session_state.df = None
if "raw_df" not in st.session_state:
    st.session_state.raw_df = None
if "filename" not in st.session_state:
    st.session_state.filename = None
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "api_provider" not in st.session_state:
    st.session_state.api_provider = "mock"
if "vector_store" not in st.session_state:
    st.session_state.vector_store = InMemoryVectorStore()
if "embedding_generator" not in st.session_state:
    st.session_state.embedding_generator = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Inject custom CSS
inject_premium_css()

# Sidebar Layout
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #00E5FF;'>🛠️ Analyst Controls</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # 1. Dataset Upload
    st.markdown("### 1. Ingest Dataset")
    uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx", "xls"])
    
    if uploaded_file is not None:
        if st.session_state.filename != uploaded_file.name:
            # New file uploaded
            try:
                with st.spinner("Loading and parsing dataset..."):
                    df = load_data(uploaded_file)
                    is_valid, errors = validate_dataframe(df)
                    
                    if is_valid:
                        st.session_state.df = df
                        st.session_state.raw_df = df.copy()
                        st.session_state.filename = uploaded_file.name
                        
                        # Trigger Vector Store indexing for RAG
                        st.session_state.vector_store.clear()
                        # Instantiate defaults
                        generator = EmbeddingGenerator(
                            use_provider=st.session_state.api_provider,
                            api_key=st.session_state.api_key
                        )
                        st.session_state.embedding_generator = generator
                        
                        # Process chunks
                        chunks = convert_dataframe_to_chunks(df, dataset_name=uploaded_file.name)
                        embeddings = generator.get_embeddings([c["text"] for c in chunks])
                        st.session_state.vector_store.add_documents(chunks, embeddings)
                        
                        st.success(f"Successfully loaded '{uploaded_file.name}'!")
                    else:
                        st.error(f"Validation failed: {', '.join(errors)}")
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
                
    st.markdown("---")
    
    # 2. LLM Configuration
    st.markdown("### 2. AI Settings")
    provider = st.selectbox(
        "LLM Provider",
        options=["mock", "gemini", "openai"],
        index=0,
        help="Select 'mock' for local heuristic answers without API keys, or connect to Gemini/OpenAI."
    )
    
    api_key = st.text_input("Enter API Key", type="password", value=st.session_state.api_key)
    
    # Update AI settings when they change
    if provider != st.session_state.api_provider or api_key != st.session_state.api_key:
        st.session_state.api_provider = provider
        st.session_state.api_key = api_key
        # Re-initialize embedding generator if dataset is active
        if st.session_state.df is not None:
            generator = EmbeddingGenerator(use_provider=provider, api_key=api_key)
            st.session_state.embedding_generator = generator
            # Reindex
            st.session_state.vector_store.clear()
            chunks = convert_dataframe_to_chunks(st.session_state.df, dataset_name=st.session_state.filename)
            embeddings = generator.get_embeddings([c["text"] for c in chunks])
            st.session_state.vector_store.add_documents(chunks, embeddings)
            st.toast("AI context re-indexed.")

# Main Page Layout
st.markdown("<h1 style='text-align: center; color: #FFFFFF;'>⚡ AI Business Analyst ⚡</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8A99AD; font-size: 1.1rem;'>The next-generation autonomous business intelligence and forecasting agent.</p>", unsafe_allow_html=True)
st.markdown("---")

# UI columns
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Welcome to Your AI Workspace")
    st.markdown("""
    This platform integrates advanced data analytics, statistical modeling, and Retrieval-Augmented Generation (RAG) 
    to provide an automated workspace for processing raw business tables.
    
    #### How to use:
    1. **Upload your dataset** in the sidebar (CSV or Excel).
    2. **Review Data Quality** in the *Data Quality* page to clean/impute values.
    3. **Visualize Insights** dynamically using the *Exploratory Analysis* portal.
    4. **Generate Forecasts** and predict seasonal trends with the *Forecasting* engine.
    5. **Chat with Data** on the *AI Chat* screen to get natural language answers to business queries.
    """)
    
    st.info("💡 **Tip:** Use the sidebar controls to toggle between OpenAI, Gemini, and a fast local fallback mode.")

with col2:
    st.markdown("### System Status")
    if st.session_state.df is not None:
        st.markdown(f"**Loaded File:** `{st.session_state.filename}`")
        
        # Render neat layout metrics
        df_shape = st.session_state.df.shape
        render_metric_card("Row Count", f"{df_shape[0]:,}", "Active Rows", "neutral")
        render_metric_card("Dimension Count", f"{df_shape[1]} columns", "Active Schema", "neutral")
    else:
        st.warning("No active dataset. Upload a file in the sidebar controller to begin.")
