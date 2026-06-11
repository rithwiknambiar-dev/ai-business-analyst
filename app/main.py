import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from src.ingestion.data_loader import DataLoader
from src.profiling.data_profiler import DataProfiler
from src.preprocessing.data_cleaner import DataCleaner
from src.eda.exploratory_analysis import ExploratoryAnalysis
from src.insights.insight_generator import InsightGenerator

from app.utils.data_manager import DataManager


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="AI Business Analyst",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("📊 AI Business Analyst")

st.markdown(
    """
    Upload a sales dataset and automatically generate:
    
    - Data Quality Reports
    - Exploratory Analysis
    - Business Insights
    - Executive Summaries
    """
)

st.markdown("---")

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("Dataset Management")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV Dataset",
    type=["csv"]
)

# --------------------------------------------------
# DATA LOADING
# --------------------------------------------------

if uploaded_file:

    df = DataManager.save_uploaded_data(
        uploaded_file
    )

    st.sidebar.success(
        "Dataset Uploaded Successfully"
    )

else:

    uploaded_df = DataManager.get_data()

    if uploaded_df is not None:

        df = uploaded_df

    else:

        df = DataLoader.load_data()

        st.sidebar.info(
            "Using Default Dataset"
        )

# --------------------------------------------------
# PROCESSING PIPELINE
# --------------------------------------------------

profiler = DataProfiler(df)

profile_report = profiler.generate_profile()

cleaner = DataCleaner(df)

cleaning_report = (
    cleaner.generate_cleaning_report()
)

eda = ExploratoryAnalysis(df)

eda_report = eda.generate_eda_report()

insight_generator = InsightGenerator(
    eda_report
)

insights = (
    insight_generator.generate_all_insights()
)

# --------------------------------------------------
# DATASET OVERVIEW
# --------------------------------------------------

st.header("Dataset Overview")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Rows",
        profile_report["rows"]
    )

with col2:

    st.metric(
        "Columns",
        profile_report["columns"]
    )

with col3:

    st.metric(
        "Memory Usage (MB)",
        profile_report["memory_usage_mb"]
    )

st.markdown("---")

# --------------------------------------------------
# DATA QUALITY
# --------------------------------------------------

st.header("Data Quality Report")

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Duplicate Rows",
        cleaning_report["duplicate_rows"]
    )

with col2:

    total_missing = sum(
        cleaning_report[
            "missing_values"
        ].values()
    )

    st.metric(
        "Missing Values",
        total_missing
    )

st.markdown("---")

# --------------------------------------------------
# EDA SUMMARY
# --------------------------------------------------

st.header("EDA Summary")

col1, col2 = st.columns(2)

with col1:

    st.subheader("Sales Summary")

    st.json(
        eda_report[
            "sales_summary"
        ]
    )

with col2:

    st.subheader("Profit Summary")

    st.json(
        eda_report[
            "profit_summary"
        ]
    )

st.markdown("---")

# --------------------------------------------------
# BUSINESS INSIGHTS
# --------------------------------------------------

st.header("Business Insights")

for idx, insight in enumerate(
    insights,
    start=1
):

    st.success(
        f"Insight {idx}: {insight}"
    )

# --------------------------------------------------
# DATA PREVIEW
# --------------------------------------------------

st.markdown("---")

with st.expander(
    "View Dataset Preview"
):

    st.dataframe(
        df.head(100),
        use_container_width=True
    )