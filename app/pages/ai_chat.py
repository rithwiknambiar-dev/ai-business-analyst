import streamlit as st
from src.utils.helpers import inject_premium_css
from src.rag.retriever import RAGRetriever
from src.rag.llm_handler import LLMHandler

st.set_page_config(page_title="AI Chat Space", page_icon="💬", layout="wide")
inject_premium_css()

st.title("💬 AI Data Chat Space")
st.markdown("---")

df = st.session_state.get("df")

if df is None:
    st.warning("⚠️ Please load a dataset first by navigating to the home page or uploading in the sidebar.")
elif st.session_state.embedding_generator is None:
    st.warning("⚠️ Chat knowledge base is not indexed. Please index your dataset from the Home page or Data Quality wizard.")
else:
    # Set up chat window and RAG layers
    vector_store = st.session_state.vector_store
    generator = st.session_state.embedding_generator
    
    retriever = RAGRetriever(vector_store, generator)
    llm = LLMHandler(
        provider=st.session_state.api_provider,
        api_key=st.session_state.api_key
    )
    
    # 2 Column layout: Chat interface & retrieved context review
    ccol1, ccol2 = st.columns([2, 1])
    
    with ccol1:
        st.markdown("### Ask Your Data")
        st.markdown("Type any natural language business questions below (e.g., *'What is the highest performing region by sales?'* or *'Summarize our revenue trend'*).")
        
        # Display existing message history
        for msg in st.session_state.chat_history:
            role = msg["role"]
            avatar = "🤖" if role == "assistant" else "👤"
            with st.chat_message(role, avatar=avatar):
                st.markdown(msg["content"])
                
        # Handle new inputs
        user_input = st.chat_input("Enter your message here...")
        
        if user_input:
            # 1. User message representation
            with st.chat_message("user", avatar="👤"):
                st.markdown(user_input)
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            # 2. Vector search & response generation
            with st.spinner("Analyzing records..."):
                retrieved_chunks = retriever.retrieve(user_input, k=3)
                
                # Generate
                answer = llm.generate_response(
                    query=user_input, 
                    retrieved_contexts=retrieved_chunks,
                    fallback_df=df
                )
                
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(answer)
            st.session_state.chat_history.append({"role": "assistant", "content": answer, "contexts": retrieved_chunks})
            st.rerun()
            
    with ccol2:
        st.markdown("### 🔍 RAG Retrieval Sources")
        st.markdown("Inspect the specific data rows or stats chunks the AI extracted from the dataset to construct its latest response.")
        
        # Pull last assistant response contexts
        last_contexts = []
        for msg in reversed(st.session_state.chat_history):
            if msg["role"] == "assistant" and "contexts" in msg:
                last_contexts = msg["contexts"]
                break
                
        if last_contexts:
            for idx, doc in enumerate(last_contexts):
                source_meta = doc.get("metadata", {})
                source_type = source_meta.get("source", "unknown")
                
                with st.expander(f"Context {idx + 1} - Source: {source_type.upper()}", expanded=True):
                    # Show clean text snippet
                    st.text(doc["text"])
                    if "start_row" in source_meta:
                        st.caption(f"Rows: {source_meta['start_row']} - {source_meta['end_row']}")
        else:
            st.caption("No retrieval triggers yet. Type a question on the left to activate RAG search.")
            
    # Clear chat utility
    if st.sidebar.button("Clear Chat Dialogue", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()
