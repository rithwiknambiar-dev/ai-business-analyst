import pandas as pd
import numpy as np

def identify_kpi_columns(df: pd.DataFrame) -> dict:
    """
    Search column names to guess which ones represent dates, numeric metrics, and categorical dimensions.
    """
    cols = df.columns
    date_col = None
    metric_cols = []
    dimension_cols = []
    
    # Identify date column
    for col in cols:
        col_lower = str(col).lower()
        # Direct date/time keywords
        if any(kw in col_lower for kw in ["date", "time", "timestamp", "year", "month", "day", "created_at"]):
            date_col = col
            break
            
    # If no date keywords, check dataframe types
    if not date_col:
        for col in cols:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                date_col = col
                break
                
    # Identify numeric metrics
    for col in cols:
        if col == date_col:
            continue
        col_lower = str(col).lower()
        if pd.api.types.is_numeric_dtype(df[col]):
            # Check unique values to distinguish keys/IDs
            if df[col].nunique() > 2 and not any(kw in col_lower for kw in ["id", "zip", "code", "phone"]):
                metric_cols.append(col)
                
    # Identify dimensions
    for col in cols:
        if col == date_col or col in metric_cols:
            continue
        # Categorical columns with relatively low cardinality
        if df[col].nunique() <= 30 or df[col].dtype == 'object' or isinstance(df[col].dtype, pd.CategoricalDtype):
            dimension_cols.append(col)
            
    return {
        "date_column": date_col,
        "metric_columns": metric_cols,
        "dimension_columns": dimension_cols
    }

def calculate_time_metrics(df: pd.DataFrame, date_col: str, metric_col: str) -> dict:
    """
    Calculate period-over-period and summary metrics for a numerical column based on a date column.
    """
    if date_col not in df.columns or metric_col not in df.columns:
        return {}
        
    df = df.copy()
    # Ensure date is parsed
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df = df.dropna(subset=[date_col])
    
    # Extract year-month for grouping
    df['YearMonth'] = df[date_col].dt.to_period('M')
    
    # Monthly aggregation
    monthly = df.groupby('YearMonth')[metric_col].sum().reset_index()
    monthly = monthly.sort_values('YearMonth')
    
    # Calculate MoM change
    monthly['growth'] = monthly[metric_col].pct_change() * 100
    
    total_val = df[metric_col].sum()
    mean_val = df[metric_col].mean()
    num_records = len(df)
    
    current_month_val = 0
    mom_growth = 0.0
    
    if not monthly.empty:
        current_month_val = monthly.iloc[-1][metric_col]
        if len(monthly) > 1:
            mom_growth = monthly.iloc[-1]['growth']
            
    return {
        "total_value": float(total_val),
        "average_value": float(mean_val) if not pd.isna(mean_val) else 0,
        "num_records": int(num_records),
        "current_month_value": float(current_month_val),
        "mom_growth_percent": float(mom_growth) if not pd.isna(mom_growth) else 0.0,
        "monthly_trend": {str(k): float(v) for k, v in zip(monthly['YearMonth'], monthly[metric_col])}
    }
