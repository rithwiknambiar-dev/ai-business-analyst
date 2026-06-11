import pytest
import pandas as pd
import tempfile
import os
from src.ingestion.data_loader import load_data, validate_dataframe

def test_load_data_csv():
    # Create temp CSV file
    with tempfile.NamedTemporaryFile(suffix=".csv", mode="w+", delete=False) as f:
        f.write("date,sales,category\n2026-01-01,100,A\n2026-01-02,200,B\n")
        temp_path = f.name
        
    try:
        df = load_data(temp_path)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
        assert list(df.columns) == ["date", "sales", "category"]
    finally:
        os.unlink(temp_path)

def test_validate_dataframe_empty():
    empty_df = pd.DataFrame()
    is_valid, errors = validate_dataframe(empty_df)
    assert not is_valid
    assert "empty" in errors[0].lower()
