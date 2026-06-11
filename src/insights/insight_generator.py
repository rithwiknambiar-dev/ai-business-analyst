import pandas as pd
import numpy as np
from src.kpi.kpi_engine import identify_kpi_columns, calculate_time_metrics
from src.anomaly_detection.anomaly_detector import detect_anomalies_zscore

def generate_automated_insights(df: pd.DataFrame) -> list[dict]:
    """
    Generate automatic natural language insights based on data properties and metrics.
    Returns a list of dicts: {"title": str, "description": str, "type": "info"|"warning"|"success"}
    """
    insights = []
    
    # 1. Column Identification
    kpis = identify_kpi_columns(df)
    date_col = kpis["date_column"]
    metrics = kpis["metric_columns"]
    dimensions = kpis["dimension_columns"]
    
    if not metrics:
        insights.append({
            "title": "Data Characteristics",
            "description": f"The dataset contains {len(df)} rows and {len(df.columns)} columns, but no clear continuous numerical columns were identified for aggregation.",
            "type": "info"
        })
        return insights
        
    primary_metric = metrics[0]
    
    # 2. General Stats Insight
    total_val = df[primary_metric].sum()
    mean_val = df[primary_metric].mean()
    insights.append({
        "title": f"Summary of {primary_metric}",
        "description": f"Total accumulated {primary_metric} is **{total_val:,.2f}** with an average value per transaction/record of **{mean_val:,.2f}** across {len(df):,} records.",
        "type": "success"
    })
    
    # 3. Categorical distribution insights
    if dimensions:
        primary_dim = dimensions[0]
        # Calculate largest categories
        cat_counts = df.groupby(primary_dim).size().reset_index(name="counts")
        if not cat_counts.empty:
            top_cat = cat_counts.sort_values(by="counts", ascending=False).iloc[0]
            insights.append({
                "title": f"Primary Segment: {primary_dim}",
                "description": f"The category **'{top_cat[primary_dim]}'** has the highest activity, representing **{top_cat['counts'] / len(df) * 100:.1f}%** ({top_cat['counts']:,} records) of the dataset.",
                "type": "info"
            })
            
        # Metric by dimension insights
        if len(metrics) > 0:
            agg_dim = df.groupby(primary_dim)[primary_metric].sum().reset_index()
            if not agg_dim.empty:
                top_agg = agg_dim.sort_values(by=primary_metric, ascending=False).iloc[0]
                insights.append({
                    "title": f"Top Volume Driver: {primary_dim}",
                    "description": f"The segment **'{top_agg[primary_dim]}'** contributed the most to {primary_metric}, totaling **{top_agg[primary_metric]:,.2f}** (**{top_agg[primary_metric] / total_val * 100:.1f}%**).",
                    "type": "success"
                })
                
    # 4. Time-series growth insights
    if date_col:
        time_stats = calculate_time_metrics(df, date_col, primary_metric)
        if time_stats and "mom_growth_percent" in time_stats:
            growth = time_stats["mom_growth_percent"]
            direction = "increased" if growth > 0 else "decreased"
            status_type = "success" if growth > 0 else "warning"
            insights.append({
                "title": f"Monthly Growth of {primary_metric}",
                "description": f"Recent monthly statistics show that {primary_metric} has **{direction} by {abs(growth):.2f}%** Month-over-Month, ending at a monthly volume of **{time_stats['current_month_value']:,.2f}**.",
                "type": status_type
            })
            
    # 5. Outlier/Anomaly insights
    anomalies = detect_anomalies_zscore(df, primary_metric)
    if not anomalies.empty:
        insights.append({
            "title": f"Anomalies Flagged in {primary_metric}",
            "description": f"We detected **{len(anomalies)} statistical anomalies** in {primary_metric} using Z-score boundaries. These instances deviate significantly from typical values and warrant further investigation.",
            "type": "warning"
        })
        
    return insights
