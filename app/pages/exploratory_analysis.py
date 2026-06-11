import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from src.utils.helpers import inject_premium_css
from src.eda.exploratory_analysis import (
    generate_correlation_matrix, 
    generate_distribution_plot, 
    generate_categorical_bar, 
    generate_relationship_plot
)

st.set_page_config(page_title="Exploratory Analysis Portal", page_icon="🔍", layout="wide")
inject_premium_css()

st.title("🔍 Exploratory Data Analysis (EDA)")
st.markdown("---")

df = st.session_state.get("df")

if df is None:
    st.warning("⚠️ Please load a dataset first by navigating to the home page or uploading in the sidebar.")
else:
    # 2 Tabs: Correlation Matrix, Chart Builder
    tab1, tab2 = st.tabs(["📊 Correlation & Matrix Maps", "🎨 Interactive Chart Builder"])
    
    with tab1:
        st.markdown("### Numerical Correlation Heatmap")
        st.markdown("Explores linear dependencies between quantitative attributes. Values near 1 or -1 express strong relationships.")
        
        # Plot correlation heatmap
        try:
            fig_corr = generate_correlation_matrix(df)
            if fig_corr:
                st.plotly_chart(fig_corr, use_container_width=True)
            else:
                st.warning("Not enough numeric columns found in the dataset to calculate a correlation matrix.")
        except Exception as e:
            st.error(f"Error drawing correlation heatmap: {str(e)}")
            
    with tab2:
        st.markdown("### Drag-and-Drop Visualizer")
        st.markdown("Design interactive charts on the fly using your active fields.")
        
        # Design Inputs sidebar-like columns
        ccol1, ccol2 = st.columns([1, 3])
        
        with ccol1:
            st.markdown("#### Configuration")
            chart_type = st.selectbox(
                "Chart Type",
                options=["Scatter Plot", "Line Chart", "Bar Chart", "Histogram", "Box Plot"]
            )
            
            # Select columns
            all_cols = list(df.columns)
            x_col = st.selectbox("X-Axis Variable", options=all_cols)
            
            # Conditionally choose Y-Axis depending on chart type
            y_col = None
            if chart_type in ["Scatter Plot", "Line Chart", "Bar Chart"]:
                y_col = st.selectbox("Y-Axis Variable", options=[None] + all_cols)
                
            color_col = st.selectbox("Group By / Color", options=[None] + all_cols)
            
            # Bar aggregations
            agg_func = None
            if chart_type == "Bar Chart" and y_col is not None:
                agg_func = st.selectbox("Aggregation Function", options=["count", "sum", "mean"])
                
        with ccol2:
            st.markdown("#### Generated Visualization")
            
            try:
                fig = None
                if chart_type == "Scatter Plot" and y_col:
                    fig = generate_relationship_plot(df, x_col, y_col, color_col, plot_type="scatter")
                elif chart_type == "Line Chart" and y_col:
                    fig = generate_relationship_plot(df, x_col, y_col, color_col, plot_type="line")
                elif chart_type == "Bar Chart":
                    fig = generate_categorical_bar(df, x_col, y_col, agg_func or "count")
                elif chart_type == "Histogram":
                    fig = generate_distribution_plot(df, x_col, plot_type="histogram")
                elif chart_type == "Box Plot":
                    fig = generate_distribution_plot(df, x_col, plot_type="box")
                    
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("Configure variables in the sidebar layout. Ensure X and Y coordinates are selected.")
            except Exception as e:
                st.error(f"Could not build visualization: {str(e)}")
