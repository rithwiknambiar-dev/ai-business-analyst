import pandas as pd
import numpy as np

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names: strip spaces, convert to lowercase, replace spaces with underscores.
    """
    df = df.copy()
    cleaned_cols = []
    for col in df.columns:
        col_str = str(col).strip().lower()
        col_str = col_str.replace(" ", "_").replace("-", "_").replace(".", "_")
        # Keep alphanumeric and underscores only
        col_str = "".join(c for c in col_str if c.isalnum() or c == "_")
        # Ensure name isn't blank
        if not col_str:
            col_str = f"column_{len(cleaned_cols)}"
        cleaned_cols.append(col_str)
        
    df.columns = cleaned_cols
    return df

def impute_missing(df: pd.DataFrame, column: str, strategy: str, custom_val=None) -> pd.DataFrame:
    """
    Impute missing values using various strategies: mean, median, mode, constant, or forward-fill/back-fill.
    """
    df = df.copy()
    if column not in df.columns:
        return df
        
    if strategy == "mean":
        if pd.api.types.is_numeric_dtype(df[column]):
            fill_val = df[column].mean()
            df[column] = df[column].fillna(fill_val)
    elif strategy == "median":
        if pd.api.types.is_numeric_dtype(df[column]):
            fill_val = df[column].median()
            df[column] = df[column].fillna(fill_val)
    elif strategy == "mode":
        mode_series = df[column].mode()
        if not mode_series.empty:
            df[column] = df[column].fillna(mode_series[0])
    elif strategy == "constant":
        df[column] = df[column].fillna(custom_val)
    elif strategy == "ffill":
        df[column] = df[column].ffill()
    elif strategy == "bfill":
        df[column] = df[column].bfill()
        
    return df

def drop_duplicates_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop duplicate records.
    """
    return df.drop_duplicates()

def parse_column_types(df: pd.DataFrame, column: str, target_type: str) -> pd.DataFrame:
    """
    Safely cast column types to numeric, datetime, categorical, or string.
    """
    df = df.copy()
    if column not in df.columns:
        return df
        
    try:
        if target_type == "numeric":
            # Strip currencies/symbols if string
            if df[column].dtype == 'object':
                df[column] = df[column].astype(str).str.replace('$', '', regex=False) \
                                                    .str.replace(',', '', regex=False) \
                                                    .str.replace('%', '', regex=False)
            df[column] = pd.to_numeric(df[column], errors='coerce')
        elif target_type == "datetime":
            df[column] = pd.to_datetime(df[column], errors='coerce')
        elif target_type == "categorical":
            df[column] = df[column].astype('category')
        elif target_type == "string":
            df[column] = df[column].astype(str)
    except Exception:
        # If conversion fails, return original
        pass
        
    return df
