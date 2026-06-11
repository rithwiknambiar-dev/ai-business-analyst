import pandas as pd
import numpy as np

def convert_dataframe_to_chunks(df: pd.DataFrame, dataset_name="dataset", rows_per_chunk=10) -> list[dict]:
    """
    Transform a pandas DataFrame into natural language text chunks for semantic indexing.
    Returns a list of dicts: [{"text": str, "metadata": dict}]
    """
    chunks = []
    num_rows = len(df)
    
    # Chunk 0: Schema and Structure Summary
    schema_text = f"Dataset: {dataset_name}\n"
    schema_text += f"Total Rows: {num_rows}, Total Columns: {len(df.columns)}\n"
    schema_text += "Columns and Types:\n"
    for col in df.columns:
        schema_text += f"- {col} (dtype: {df[col].dtype})\n"
    
    chunks.append({
        "text": schema_text,
        "metadata": {"source": "schema_summary", "dataset": dataset_name}
    })
    
    # Chunk 1: General Summary Stats
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    stats_text = f"Statistical Summary of {dataset_name}:\n"
    for col in numeric_cols:
        col_min = df[col].min()
        col_max = df[col].max()
        col_mean = df[col].mean()
        stats_text += f"- Column '{col}': Min = {col_min}, Max = {col_max}, Average = {col_mean:.2f}\n"
        
    chunks.append({
        "text": stats_text,
        "metadata": {"source": "stats_summary", "dataset": dataset_name}
    })
    
    # Row Chunks: Convert multiple rows to textual descriptions
    for start_idx in range(0, num_rows, rows_per_chunk):
        end_idx = min(start_idx + rows_per_chunk, num_rows)
        sub_df = df.iloc[start_idx:end_idx]
        
        chunk_text = f"Records {start_idx + 1} to {end_idx} in {dataset_name}:\n"
        for idx, row in sub_df.iterrows():
            row_desc = f"- Row {idx + 1}: "
            fields = []
            for col in df.columns:
                fields.append(f"{col} is '{row[col]}'")
            row_desc += ", ".join(fields) + "\n"
            chunk_text += row_desc
            
        chunks.append({
            "text": chunk_text,
            "metadata": {
                "source": "data_rows",
                "dataset": dataset_name,
                "start_row": start_idx + 1,
                "end_row": end_idx
            }
        })
        
    return chunks
