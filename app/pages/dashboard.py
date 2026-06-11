import sys
from pathlib import Path

import streamlit as st
import plotly.express as px

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

from src.ingestion.data_loader import DataLoader


st.set_page_config(
    page_title="Dashboard",
    layout="wide"
)

st.title("Business Dashboard")

# Load Data
df = DataLoader.load_data()

# KPIs

total_sales = round(df["Sales"].sum(), 2)

total_profit = round(df["Profit"].sum(), 2)

profit_margin = round(
    (total_profit / total_sales) * 100,
    2
)

total_orders = df["Order ID"].nunique()

# KPI SECTION

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Sales",
        f"${total_sales:,.0f}"
    )

with col2:
    st.metric(
        "Total Profit",
        f"${total_profit:,.0f}"
    )

with col3:
    st.metric(
        "Profit Margin",
        f"{profit_margin}%"
    )

with col4:
    st.metric(
        "Total Orders",
        total_orders
    )

st.markdown("---")

# SALES BY REGION

region_sales = (
    df.groupby("Region")["Sales"]
    .sum()
    .reset_index()
)

fig_region_sales = px.bar(
    region_sales,
    x="Region",
    y="Sales",
    title="Sales by Region"
)

st.plotly_chart(
    fig_region_sales,
    use_container_width=True
)

# PROFIT BY REGION

region_profit = (
    df.groupby("Region")["Profit"]
    .sum()
    .reset_index()
)

fig_region_profit = px.bar(
    region_profit,
    x="Region",
    y="Profit",
    title="Profit by Region"
)

st.plotly_chart(
    fig_region_profit,
    use_container_width=True
)

# SALES BY CATEGORY

category_sales = (
    df.groupby("Category")["Sales"]
    .sum()
    .reset_index()
)

fig_category_sales = px.pie(
    category_sales,
    names="Category",
    values="Sales",
    title="Sales by Category"
)

st.plotly_chart(
    fig_category_sales,
    use_container_width=True
)

# SALES BY SEGMENT

segment_sales = (
    df.groupby("Segment")["Sales"]
    .sum()
    .reset_index()
)

fig_segment_sales = px.pie(
    segment_sales,
    names="Segment",
    values="Sales",
    title="Sales by Segment"
)

st.plotly_chart(
    fig_segment_sales,
    use_container_width=True
)

st.markdown("---")

# BEST REGION

best_region = (
    df.groupby("Region")["Sales"]
    .sum()
    .idxmax()
)

worst_region = (
    df.groupby("Region")["Sales"]
    .sum()
    .idxmin()
)

col1, col2 = st.columns(2)

with col1:
    st.success(
        f"Best Performing Region: {best_region}"
    )

with col2:
    st.error(
        f"Worst Performing Region: {worst_region}"
    )