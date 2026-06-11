import pandas as pd
import numpy as np

def profile_dataset(df: pd.DataFrame) -> dict:
    """
    Profile a dataframe and calculate various data quality and type characteristics.
    """
    num_rows = len(df)
    num_cols = len(df.columns)
    
    # Calculate duplicates
    num_duplicate_rows = df.duplicated().sum()
    pct_duplicate_rows = (num_duplicate_rows / num_rows * 100) if num_rows > 0 else 0
    
    columns_profile = {}
    total_missing_cells = 0
    total_cells = num_rows * num_cols
    
    for col in df.columns:
        col_data = df[col]
        missing_count = col_data.isna().sum()
        total_missing_cells += missing_count
        missing_pct = (missing_count / num_rows * 100) if num_rows > 0 else 0
        
        unique_count = col_data.nunique()
        unique_pct = (unique_count / num_rows * 100) if num_rows > 0 else 0
        
        # Determine semantic/inferred data type
        inferred_type = "text"
        sample_values = col_data.dropna().head(100)
        
        # 1. Check if datetime
        is_date = False
        if pd.api.types.is_datetime64_any_dtype(col_data):
            is_date = True
        else:
            # Try parsing a sample as date
            if len(sample_values) > 0:
                try:
                    # Avoid parsing simple numbers as dates
                    if not pd.api.types.is_numeric_dtype(sample_values):
                        pd.to_datetime(sample_values, errors='raise')
                        is_date = True
                except (ValueError, TypeError, OverflowError):
                    pass
                    
        if is_date:
            inferred_type = "datetime"
        elif pd.api.types.is_numeric_dtype(col_data):
            # Check if boolean-like or binary
            if unique_count <= 2:
                vals = set(str(v).strip().lower() for v in sample_values)
                if vals.issubset({"true", "false", "yes", "no", "y", "n", "1", "0", "1.0", "0.0"}):
                    inferred_type = "boolean"
                else:
                    inferred_type = "integer" if pd.api.types.is_integer_dtype(col_data) else "float"
            # If high ratio of unique ints, keep as numeric (integer vs float)
            elif pd.api.types.is_integer_dtype(col_data):
                inferred_type = "integer"
            else:
                inferred_type = "float"
        elif unique_count <= min(15, max(10, num_rows * 0.15)):
            inferred_type = "categorical"
        elif unique_count <= 2:
            vals = set(str(v).strip().lower() for v in sample_values)
            if vals.issubset({"true", "false", "yes", "no", "y", "n", "t", "f"}):
                inferred_type = "boolean"
            else:
                inferred_type = "categorical"
        else:
            inferred_type = "text"
            
        stats = {
            "missing_count": int(missing_count),
            "missing_pct": float(missing_pct),
            "unique_count": int(unique_count),
            "unique_pct": float(unique_pct),
            "type": inferred_type,
            "pandas_type": str(col_data.dtype)
        }
        
        # Calculate summary statistics based on inferred type
        if inferred_type in ["integer", "float"]:
            stats.update({
                "mean": float(col_data.mean()) if not col_data.empty else None,
                "std": float(col_data.std()) if not col_data.empty and len(col_data) > 1 else None,
                "min": float(col_data.min()) if not col_data.empty else None,
                "max": float(col_data.max()) if not col_data.empty else None,
                "median": float(col_data.median()) if not col_data.empty else None,
            })
        elif inferred_type == "categorical":
            value_counts = col_data.value_counts(normalize=True).head(5).to_dict()
            stats["top_categories"] = {str(k): float(v) for k, v in value_counts.items()}
        elif inferred_type == "datetime":
            try:
                parsed_dates = pd.to_datetime(col_data, errors='coerce')
                stats.update({
                    "min_date": str(parsed_dates.min()) if not parsed_dates.empty else None,
                    "max_date": str(parsed_dates.max()) if not parsed_dates.empty else None,
                })
            except Exception:
                pass
                
        columns_profile[col] = stats
        
    # Calculate Data Quality Score (0 to 100)
    # Penalties for: missing values (weight 50%), duplicates (weight 30%), cardinality imbalances (weight 20%)
    missing_ratio = (total_missing_cells / total_cells) if total_cells > 0 else 0
    duplicate_ratio = (num_duplicate_rows / num_rows) if num_rows > 0 else 0
    
    # Calculate cardinality issues (columns with only 1 unique value)
    single_val_cols = sum(1 for col_info in columns_profile.values() if col_info["unique_count"] <= 1)
    single_val_ratio = (single_val_cols / num_cols) if num_cols > 0 else 0
    
    score = 100 - (missing_ratio * 50) - (duplicate_ratio * 30) - (single_val_ratio * 20)
    quality_score = max(0.0, min(100.0, score))
    
    return {
        "num_rows": num_rows,
        "num_cols": num_cols,
        "num_duplicate_rows": int(num_duplicate_rows),
        "pct_duplicate_rows": float(pct_duplicate_rows),
        "total_missing_cells": int(total_missing_cells),
        "total_cells": int(total_cells),
        "overall_missing_pct": float(missing_ratio * 100),
        "data_quality_score": float(round(quality_score, 1)),
        "columns": columns_profile
    }
