import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from src.utils.helpers import inject_premium_css, render_metric_card
from src.kpi.kpi_engine import identify_kpi_columns, calculate_time_metrics

st.set_page_config(page_title="Executive Dashboard", page_icon="📈", layout="wide")
inject_premium_css()

st.title("📈 Executive Dashboard")
st.markdown("---")

df = st.session_state.get("df")

if df is None:
    st.warning("⚠️ Please load a dataset first by navigating to the home page or uploading in the sidebar.")
else:
    kpi_cols = identify_kpi_columns(df)
    date_col = kpi_cols["date_column"]
    metric_cols = kpi_cols["metric_columns"]
    dimension_cols = kpi_cols["dimension_columns"]
    
    if not metric_cols:
        st.warning("No numeric columns found in the dataset to calculate KPIs. Please load a dataset with metric fields.")
    else:
        # Selection of primary metrics
        st.sidebar.markdown("### Metric Configuration")
        selected_metric = st.sidebar.selectbox("Primary Metric", options=metric_cols)
        
        selected_date = None
        if date_col:
            selected_date = st.sidebar.selectbox("Date Column", options=[date_col] + [col for col in df.columns if col != date_col])
        else:
            # Check if any other datetime columns can be parsed
            date_candidates = [col for col in df.columns if "date" in col.lower() or "time" in col.lower()]
            if date_candidates:
                selected_date = st.sidebar.selectbox("Select Date Column", options=date_candidates)
                
        # Main Metrics grid
        col1, col2, col3 = st.columns(3)
        
        total_sum = df[selected_metric].sum()
        mean_val = df[selected_metric].mean()
        record_count = len(df)
        
        with col1:
            render_metric_card(f"Total {selected_metric}", f"{total_sum:,.2f}", "Accumulated sum", "up")
        with col2:
            render_metric_card(f"Average {selected_metric}", f"{mean_val:,.2f}", "Mean per record", "neutral")
        with col3:
            render_metric_card("Total Transactions / Records", f"{record_count:,}", "Total rows processed", "neutral")
            
        st.markdown("---")
        
        # Trend Chart
        if selected_date:
            try:
                # Group by Year-Month or Date
                df_temp = df.copy()
                df_temp[selected_date] = pd.to_datetime(df_temp[selected_date], errors='coerce')
                df_temp = df_temp.dropna(subset=[selected_date])
                
                # Check timeframe to decide granularity
                time_range = df_temp[selected_date].max() - df_temp[selected_date].min()
                if time_range.days > 365 * 2:
                    groupby_freq = 'YE'
                    freq_lbl = "Yearly"
                elif time_range.days > 90:
                    groupby_freq = 'ME'
                    freq_lbl = "Monthly"
                else:
                    groupby_freq = 'D'
                    freq_lbl = "Daily"
                    
                trend_df = df_temp.groupby(pd.Grouper(key=selected_date, freq=groupby_freq))[selected_metric].sum().reset_index()
                trend_df = trend_df.sort_values(selected_date)
                
                fig = px.line(
                    trend_df,
                    x=selected_date,
                    y=selected_metric,
                    title=f"{freq_lbl} Trend of {selected_metric}",
                    color_discrete_sequence=["#00E5FF"]
                )
                fig.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#FFFFFF")
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Could not construct time-trend chart: {str(e)}")
                
        # Category Breakdowns
        if dimension_cols:
            st.markdown("### Segment Performance Details")
            dim_col1, dim_col2 = st.columns(2)
            
            # Sub-column 1: First Dimension Breakdown
            with dim_col1:
                dim1 = dimension_cols[0]
                dim1_df = df.groupby(dim1)[selected_metric].sum().reset_index().sort_values(by=selected_metric, ascending=False).head(10)
                fig1 = px.bar(
                    dim1_df,
                    x=dim1,
                    y=selected_metric,
                    title=f"Top 10 {dim1} by {selected_metric}",
                    color=selected_metric,
                    color_continuous_scale="Purples"
                )
                fig1.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#FFFFFF")
                )
                st.plotly_chart(fig1, use_container_width=True)
                
            # Sub-column 2: Second Dimension or Pie Chart
            with dim_col2:
                dim2 = dimension_cols[1] if len(dimension_cols) > 1 else dim1
                dim2_df = df.groupby(dim2).size().reset_index(name="counts").sort_values(by="counts", ascending=False).head(8)
                fig2 = px.pie(
                    dim2_df,
                    names=dim2,
                    values="counts",
                    title=f"Record Breakdown by {dim2}",
                    color_discrete_sequence=px.colors.sequential.Agsunset
                )
                fig2.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#FFFFFF")
                )
                st.plotly_chart(fig2, use_container_width=True)
