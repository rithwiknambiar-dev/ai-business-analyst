import pytest
import pandas as pd
from src.insights.insight_generator import generate_automated_insights
from src.kpi.kpi_engine import identify_kpi_columns

def test_identify_kpi_columns():
    df = pd.DataFrame({
        "order_date": ["2026-01-01", "2026-01-02", "2026-01-03"],
        "revenue": [100.5, 200.0, 150.25],
        "customer_segment": ["Corporate", "SMB", "Corporate"],
        "phone_number": ["12345", "67890", "11223"]
    })
    
    kpis = identify_kpi_columns(df)
    assert kpis["date_column"] == "order_date"
    assert "revenue" in kpis["metric_columns"]
    assert "customer_segment" in kpis["dimension_columns"]
    # Phone number should not be classified as a primary aggregation metric or category
    assert "phone_number" not in kpis["metric_columns"]

def test_generate_automated_insights():
    df = pd.DataFrame({
        "date": pd.date_range("2026-01-01", periods=100),
        "sales": range(100),
        "region": ["East", "West"] * 50
    })
    
    insights = generate_automated_insights(df)
    assert len(insights) > 0
    # Checks that insights contain title, description, and status types
    assert "title" in insights[0]
    assert "description" in insights[0]
    assert "type" in insights[0]
