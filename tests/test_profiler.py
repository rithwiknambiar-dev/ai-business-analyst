import pytest
import pandas as pd
import numpy as np
from src.profiling.data_profiler import profile_dataset

def test_profile_dataset():
    # Construct synthetic data
    df = pd.DataFrame({
        "dates": pd.date_range(start="2026-01-01", periods=10),
        "values": [1.5, 2.5, 3.5, np.nan, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5],
        "label": ["A", "B", "A", "B", "A", "B", "A", "B", "A", "B"]
    })
    
    profile = profile_dataset(df)
    assert profile["num_rows"] == 10
    assert profile["num_cols"] == 3
    assert profile["total_missing_cells"] == 1
    assert "values" in profile["columns"]
    assert profile["columns"]["values"]["type"] == "float"
    assert profile["columns"]["label"]["type"] == "categorical"
    assert profile["data_quality_score"] > 50.0  # Should be decent
