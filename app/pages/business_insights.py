import sys
from pathlib import Path

import streamlit as st

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

from src.ingestion.data_loader import DataLoader
from src.eda.exploratory_analysis import ExploratoryAnalysis
from src.insights.insight_generator import InsightGenerator


st.set_page_config(
    page_title="Business Insights",
    layout="wide"
)

st.title("Business Insights & Recommendations")

# ---------------------------------------
# Load Data
# ---------------------------------------

df = DataLoader.load_data()

eda = ExploratoryAnalysis(df)

eda_report = eda.generate_eda_report()

insight_generator = InsightGenerator(
    eda_report
)

insights = insight_generator.generate_all_insights()

# ---------------------------------------
# Executive Summary
# ---------------------------------------

st.header("Executive Summary")

for insight in insights:

    st.success(insight)

st.markdown("---")

# ---------------------------------------
# Key Findings
# ---------------------------------------

st.header("Key Findings")

region = eda_report[
    "region_analysis"
]["best_region"]

category = eda_report[
    "category_analysis"
]["best_category"]

segment_sales = eda_report[
    "segment_analysis"
]["sales_by_segment"]

top_segment = max(
    segment_sales,
    key=segment_sales.get
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Best Region",
        region
    )

with col2:

    st.metric(
        "Best Category",
        category
    )

with col3:

    st.metric(
        "Top Segment",
        top_segment
    )

st.markdown("---")

# ---------------------------------------
# Recommendations
# ---------------------------------------

st.header("Business Recommendations")

recommendations = [

    "Increase investment in high-performing regions.",

    "Focus on Technology products to maximize profit.",

    "Reduce excessive discounting strategies.",

    "Improve performance in low-revenue regions.",

    "Target Consumer customers with retention campaigns."

]

for rec in recommendations:

    st.info(rec)