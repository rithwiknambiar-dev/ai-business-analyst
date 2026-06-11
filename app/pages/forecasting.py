import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from src.utils.helpers import inject_premium_css, render_metric_card
from src.kpi.kpi_engine import identify_kpi_columns
from src.forecasting.forecast_engine import generate_forecast

st.set_page_config(page_title="Trend Forecasting", page_icon="🔮", layout="wide")
inject_premium_css()

st.title("🔮 Predictive Forecasting Engine")
st.markdown("---")

df = st.session_state.get("df")

if df is None:
    st.warning("⚠️ Please load a dataset first by navigating to the home page or uploading in the sidebar.")
else:
    # Identify kpis
    kpi_cols = identify_kpi_columns(df)
    date_col = kpi_cols["date_column"]
    metric_cols = kpi_cols["metric_columns"]
    
    if not date_col:
        st.warning("No time-series date column detected in the dataset. Please load a dataset containing chronological dates to activate forecasting.")
    elif not metric_cols:
        st.warning("No numerical metrics found for forecasting.")
    else:
        # Forecast control columns
        fcol1, fcol2 = st.columns([1, 3])
        
        with fcol1:
            st.markdown("#### Forecast Configuration")
            target_metric = st.selectbox("Target Metric", options=metric_cols)
            date_field = st.selectbox("Time Axis Column", options=[date_col] + [col for col in df.columns if col != date_col])
            
            # Select frequency
            freq = st.selectbox(
                "Aggregating Frequency",
                options=[("Monthly", "M"), ("Weekly", "W"), ("Daily", "D")],
                format_func=lambda x: x[0]
            )[1]
            
            horizon = st.slider("Forecast Horizon (periods ahead)", min_value=3, max_value=24, value=6)
            
            run_btn = st.button("Generate Projections", type="primary", use_container_width=True)
            
        with fcol2:
            st.markdown("#### Future Trend Forecast")
            
            if run_btn:
                with st.spinner("Training predictive models..."):
                    forecast_df, status = generate_forecast(
                        df, 
                        date_col=date_field, 
                        target_col=target_metric, 
                        horizon=horizon, 
                        freq=freq
                    )
                    
                if not forecast_df.empty:
                    st.success(status)
                    
                    # Separate history and forecast for rendering
                    history = forecast_df[~forecast_df["Is_Forecast"]]
                    future = forecast_df[forecast_df["Is_Forecast"]]
                    
                    # Create Plotly figure with confidence bands
                    fig = go.Figure()
                    
                    # 1. Actual history
                    fig.add_trace(go.Scatter(
                        x=history["Date"],
                        y=history["Actual"],
                        name="Historical Actuals",
                        mode="lines+markers",
                        line=dict(color="#00E5FF", width=2.5)
                    ))
                    
                    # 2. Predicted history values (fitted)
                    fig.add_trace(go.Scatter(
                        x=history["Date"],
                        y=history["Forecast"],
                        name="Fitted Values",
                        mode="lines",
                        line=dict(color="#2979FF", width=1.5, dash="dash")
                    ))
                    
                    # 3. Future Forecast values
                    fig.add_trace(go.Scatter(
                        x=future["Date"],
                        y=future["Forecast"],
                        name="Model Forecast",
                        mode="lines+markers",
                        line=dict(color="#FF9100", width=2.5)
                    ))
                    
                    # 4. Confidence intervals
                    fig.add_trace(go.Scatter(
                        x=future["Date"],
                        y=future["Upper_CI"],
                        name="Upper Bound",
                        mode="lines",
                        line=dict(width=0),
                        showlegend=False
                    ))
                    
                    fig.add_trace(go.Scatter(
                        x=future["Date"],
                        y=future["Lower_CI"],
                        name="Confidence Band (95%)",
                        mode="lines",
                        fill="tonexty",
                        fillcolor="rgba(255, 145, 0, 0.15)",
                        line=dict(width=0),
                    ))
                    
                    fig.update_layout(
                        title=f"Predictive Forecast: {target_metric} over {date_field}",
                        xaxis_title="Timeline",
                        yaxis_title=target_metric,
                        plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)",
                        font=dict(color="#FFFFFF"),
                        hovermode="x unified"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Show data values table for forecast periods
                    st.markdown("#### Forecasted Projections Table")
                    display_future = future[["Date", "Forecast", "Lower_CI", "Upper_CI"]].copy()
                    display_future.columns = ["Date Period", "Forecast Target", "95% Lower Limit", "95% Upper Limit"]
                    st.dataframe(display_future, use_container_width=True)
                else:
                    st.error(status)
            else:
                st.info("Configure your target metric and timeframe parameters, then click 'Generate Projections' to run.")
