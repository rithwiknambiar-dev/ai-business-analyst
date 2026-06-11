import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from src.utils.helpers import inject_premium_css, render_metric_card
from src.profiling.data_profiler import profile_dataset
from src.preprocessing.data_cleaner import clean_column_names, impute_missing, drop_duplicates_df, parse_column_types

st.set_page_config(page_title="Data Quality Portal", page_icon="🛡️", layout="wide")
inject_premium_css()

st.title("🛡️ Data Quality & Cleaning Portal")
st.markdown("---")

df = st.session_state.get("df")

if df is None:
    st.warning("⚠️ Please load a dataset first by navigating to the home page or uploading in the sidebar.")
else:
    # Perform Profiling
    profile = profile_dataset(df)
    
    # Grid summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        score = profile["data_quality_score"]
        status = "up" if score > 80 else ("down" if score < 50 else "neutral")
        render_metric_card("Data Quality Score", f"{score}/100", "Overall index", status)
    with col2:
        render_metric_card("Missing Cells Ratio", f"{profile['overall_missing_pct']:.1f}%", f"{profile['total_missing_cells']:,} cells", "down" if profile['overall_missing_pct'] > 5 else "up")
    with col3:
        render_metric_card("Duplicate Rows Ratio", f"{profile['pct_duplicate_rows']:.1f}%", f"{profile['num_duplicate_rows']:,} rows", "down" if profile['num_duplicate_rows'] > 0 else "up")
    with col4:
        render_metric_card("Total Schema Columns", f"{profile['num_cols']}", "Variables active", "neutral")
        
    st.markdown("---")
    
    # 2-Column Layout for Schema details and wizard
    dcol1, dcol2 = st.columns([1, 1])
    
    with dcol1:
        st.markdown("### Column Details & Type Profiles")
        # Build schema data table
        col_list = []
        missing_list = []
        types_list = []
        uniques_list = []
        
        for name, info in profile["columns"].items():
            col_list.append(name)
            missing_list.append(f"{info['missing_pct']:.1f}% ({info['missing_count']})")
            types_list.append(info["type"])
            uniques_list.append(info["unique_count"])
            
        schema_summary_df = pd.DataFrame({
            "Column Name": col_list,
            "Inferred Type": types_list,
            "Missingness": missing_list,
            "Unique Count": uniques_list
        })
        st.dataframe(schema_summary_df, use_container_width=True)
        
        # Plot missingness distribution
        missing_counts = pd.DataFrame([
            {"Column": k, "Missing Count": v["missing_count"]} for k, v in profile["columns"].items() if v["missing_count"] > 0
        ])
        
        if not missing_counts.empty:
            st.markdown("#### Missing Cells Breakdown")
            fig = px.bar(
                missing_counts,
                x="Column",
                y="Missing Count",
                title="Cells with Missing/Null Values",
                color_discrete_sequence=["#FF1744"]
            )
            fig.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#FFFFFF")
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("🎉 Excellent! No missing values detected in the entire dataset.")
            
    with dcol2:
        st.markdown("### 🛠️ Interactive Data Cleaning Wizard")
        st.markdown("Use these modular tools to fix quality issues and transform your active schema.")
        
        # Operation 1: Normalise Column Names
        st.markdown("#### 1. Clean Column Headers")
        st.caption("Converts columns to lowercase, replaces spaces/dashes with underscores, and strips characters.")
        if st.button("Normalize Headers", use_container_width=True):
            st.session_state.df = clean_column_names(st.session_state.df)
            st.success("Headers normalized!")
            st.rerun()
            
        st.markdown("---")
        
        # Operation 2: Drop duplicates
        st.markdown("#### 2. Deduplicate Records")
        st.caption(f"Remove identical duplicate rows. Current duplicates: {profile['num_duplicate_rows']:,}")
        if st.button("Drop Duplicates", use_container_width=True):
            st.session_state.df = drop_duplicates_df(st.session_state.df)
            st.success("Duplicate records removed!")
            st.rerun()
            
        st.markdown("---")
        
        # Operation 3: Type Casting
        st.markdown("#### 3. Recast Column Types")
        st.caption("Manually override the datatype of an active column.")
        cast_col = st.selectbox("Select Target Column", options=df.columns, key="cast_col_select")
        cast_type = st.selectbox("Cast To Type", options=["numeric", "datetime", "categorical", "string"])
        if st.button("Apply Cast Type", use_container_width=True):
            st.session_state.df = parse_column_types(st.session_state.df, cast_col, cast_type)
            st.success(f"Column '{cast_col}' cast to {cast_type}!")
            st.rerun()
            
        st.markdown("---")
        
        # Operation 4: Impute Missing
        st.markdown("#### 4. Impute Missing Values")
        st.caption("Impute missing cells for numerical or categorical columns.")
        impute_col = st.selectbox("Select Column to Impute", options=[k for k, v in profile["columns"].items() if v["missing_count"] > 0]) if [k for k, v in profile["columns"].items() if v["missing_count"] > 0] else None
        
        if impute_col:
            strategy = st.selectbox("Imputation Strategy", options=["mean", "median", "mode", "constant", "ffill", "bfill"])
            custom_val = None
            if strategy == "constant":
                custom_val = st.text_input("Impute Value (Placeholder)", value="")
                
            if st.button("Impute Column Values", use_container_width=True):
                st.session_state.df = impute_missing(st.session_state.df, impute_col, strategy, custom_val)
                st.success(f"Imputed missing entries in '{impute_col}' via '{strategy}'!")
                st.rerun()
        else:
            st.success("No missing columns require imputation.")
            
        st.markdown("---")
        
        # Reset Button
        st.markdown("#### Restore Dataset")
        st.caption("Reverts all modifications and restores the raw dataset file uploaded.")
        if st.button("Reset to Original File", use_container_width=True, type="secondary"):
            st.session_state.df = st.session_state.raw_df.copy()
            st.success("Dataset reset to original upload version.")
            st.rerun()
            
        # Re-index button for vector store
        if st.button("Re-Index AI Knowledge Base", use_container_width=True, type="primary"):
            with st.spinner("Updating vector index..."):
                st.session_state.vector_store.clear()
                # Re-index
                generator = st.session_state.embedding_generator or EmbeddingGenerator(use_provider=st.session_state.api_provider, api_key=st.session_state.api_key)
                chunks = convert_dataframe_to_chunks(st.session_state.df, dataset_name=st.session_state.filename)
                embeddings = generator.get_embeddings([c["text"] for c in chunks])
                st.session_state.vector_store.add_documents(chunks, embeddings)
                st.success("RAG Knowledge base synchronized with the cleaned dataset version!")
