import sys
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px

project_root = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(project_root))

from src.ingestion.data_loader import DataLoader


st.set_page_config(
    page_title="Exploratory Analysis",
    layout="wide"
)

st.title("Exploratory Data Analysis")

# ---------------------------------------
# LOAD DATA
# ---------------------------------------

df = DataLoader.load_data()

# ---------------------------------------
# SALES BY REGION
# ---------------------------------------

st.header("Sales by Region")

region_sales = (
    df.groupby("Region")["Sales"]
    .sum()
    .reset_index()
    .sort_values(
        by="Sales",
        ascending=False
    )
)

fig_region_sales = px.bar(
    region_sales,
    x="Region",
    y="Sales",
    title="Sales by Region",
    text_auto=".2s"
)

st.plotly_chart(
    fig_region_sales,
    use_container_width=True
)

# ---------------------------------------
# PROFIT BY REGION
# ---------------------------------------

st.header("Profit by Region")

region_profit = (
    df.groupby("Region")["Profit"]
    .sum()
    .reset_index()
    .sort_values(
        by="Profit",
        ascending=False
    )
)

fig_region_profit = px.bar(
    region_profit,
    x="Region",
    y="Profit",
    title="Profit by Region",
    text_auto=".2s"
)

st.plotly_chart(
    fig_region_profit,
    use_container_width=True
)

# ---------------------------------------
# CATEGORY & SEGMENT
# ---------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.header("Sales by Category")

    category_sales = (
        df.groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig_category = px.pie(
        category_sales,
        names="Category",
        values="Sales",
        hole=0.5
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )

with col2:

    st.header("Sales by Segment")

    segment_sales = (
        df.groupby("Segment")["Sales"]
        .sum()
        .reset_index()
    )

    fig_segment = px.pie(
        segment_sales,
        names="Segment",
        values="Sales",
        hole=0.5
    )

    st.plotly_chart(
        fig_segment,
        use_container_width=True
    )

# ---------------------------------------
# TOP PRODUCTS
# ---------------------------------------

st.header("Top 10 Products by Sales")

top_products = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(
        ascending=False
    )
    .head(10)
    .reset_index()
)

fig_products = px.bar(
    top_products,
    x="Sales",
    y="Product Name",
    orientation="h",
    title="Top 10 Products"
)

fig_products.update_layout(
    yaxis={
        "categoryorder":
        "total ascending"
    }
)

st.plotly_chart(
    fig_products,
    use_container_width=True
)

# ---------------------------------------
# TOP SUB-CATEGORIES
# ---------------------------------------

st.header("Top 10 Sub-Categories")

top_subcategories = (
    df.groupby("Sub-Category")["Sales"]
    .sum()
    .sort_values(
        ascending=False
    )
    .head(10)
    .reset_index()
)

fig_subcategory = px.bar(
    top_subcategories,
    x="Sales",
    y="Sub-Category",
    orientation="h",
    title="Top Sub-Categories"
)

fig_subcategory.update_layout(
    yaxis={
        "categoryorder":
        "total ascending"
    }
)

st.plotly_chart(
    fig_subcategory,
    use_container_width=True
)

# ---------------------------------------
# MONTHLY SALES TREND
# ---------------------------------------

st.header("Monthly Sales Trend")

monthly_sales = (
    df.groupby(
        df["Order Date"].dt.to_period("M")
    )["Sales"]
    .sum()
    .reset_index()
)

monthly_sales["Order Date"] = (
    monthly_sales["Order Date"]
    .astype(str)
)

fig_trend = px.line(
    monthly_sales,
    x="Order Date",
    y="Sales",
    title="Monthly Sales Trend",
    markers=True
)

st.plotly_chart(
    fig_trend,
    use_container_width=True
)

# ---------------------------------------
# CORRELATION MATRIX
# ---------------------------------------

st.header("Correlation Analysis")

corr_df = df[
    [
        "Sales",
        "Profit",
        "Quantity",
        "Discount"
    ]
]

corr_matrix = corr_df.corr()

fig_corr = px.imshow(
    corr_matrix,
    text_auto=True,
    aspect="auto",
    title="Correlation Matrix"
)

st.plotly_chart(
    fig_corr,
    use_container_width=True
)

# ---------------------------------------
# DATA PREVIEW
# ---------------------------------------

st.header("Dataset Preview")

with st.expander(
    "Click to View Data"
):

    st.dataframe(
        df.head(100),
        use_container_width=True
    )