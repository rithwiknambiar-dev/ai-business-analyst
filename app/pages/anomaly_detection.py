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

from src.anomaly_detection.anomaly_detector import (
    detect_anomalies_zscore,
    detect_anomalies_multivariate
)

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Anomaly Detection",
    layout="wide"
)

st.title(
    "🚨 Anomaly Detection"
)

st.markdown(
    """
Identify unusual records, outliers, and suspicious business transactions.
"""
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

df = DataManager.get_data()

if df is None:

    try:

        df = DataLoader.load_data()

    except Exception:

        st.warning(
            "Please load a dataset first."
        )

        st.stop()

# --------------------------------------------------
# DATASET INFO
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Rows",
        len(df)
    )

with col2:

    st.metric(
        "Columns",
        len(df.columns)
    )

with col3:

    numeric_cols_count = len(
        df.select_dtypes(
            include=["int64", "float64"]
        ).columns
    )

    st.metric(
        "Numeric Features",
        numeric_cols_count
    )

st.markdown("---")

# --------------------------------------------------
# NUMERIC COLUMNS
# --------------------------------------------------

numeric_columns = (
    df.select_dtypes(
        include=["int64", "float64"]
    )
    .columns
    .tolist()
)

if len(numeric_columns) == 0:

    st.error(
        "No numeric columns available for anomaly detection."
    )

    st.stop()

# --------------------------------------------------
# DETECTION METHOD
# --------------------------------------------------

method = st.radio(
    "Select Detection Method",
    [
        "Z-Score",
        "Isolation Forest"
    ]
)

st.markdown("---")

# --------------------------------------------------
# Z SCORE
# --------------------------------------------------

if method == "Z-Score":

    st.subheader(
        "Z-Score Based Anomaly Detection"
    )

    selected_column = st.selectbox(
        "Select Numeric Column",
        numeric_columns
    )

    threshold = st.slider(
        "Z-Score Threshold",
        min_value=2.0,
        max_value=5.0,
        value=3.0,
        step=0.5
    )

    if st.button(
        "Run Detection"
    ):

        anomalies = (
            detect_anomalies_zscore(
                df,
                selected_column,
                threshold
            )
        )

        st.markdown("---")

        st.metric(
            "Anomalies Found",
            len(anomalies)
        )

        if len(anomalies) > 0:

            st.success(
                f"{len(anomalies)} anomalies detected."
            )

            st.dataframe(
                anomalies,
                width="stretch"
            )

        else:

            st.success(
                "No anomalies detected."
            )

# --------------------------------------------------
# ISOLATION FOREST
# --------------------------------------------------

else:

    st.subheader(
        "Isolation Forest Anomaly Detection"
    )

    selected_columns = st.multiselect(
        "Select Numeric Columns",
        numeric_columns,
        default=numeric_columns[:3]
    )

    contamination = st.slider(
        "Contamination Rate",
        min_value=0.01,
        max_value=0.20,
        value=0.05
    )

    if st.button(
        "Run Detection"
    ):

        anomalies = (
            detect_anomalies_multivariate(
                df,
                selected_columns,
                contamination
            )
        )

        st.markdown("---")

        st.metric(
            "Anomalies Found",
            len(anomalies)
        )

        if len(anomalies) > 0:

            st.success(
                f"{len(anomalies)} anomalies detected."
            )

            st.dataframe(
                anomalies,
                width="stretch"
            )

        else:

            st.success(
                "No anomalies detected."
            )

# --------------------------------------------------
# DATA PREVIEW
# --------------------------------------------------

with st.expander(
    "View Dataset Sample"
):

    st.dataframe(
        df.head(20),
        width="stretch"
    )