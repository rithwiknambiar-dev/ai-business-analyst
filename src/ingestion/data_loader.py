import pandas as pd
import io
import os
from pathlib import Path

def load_data(file_source) -> pd.DataFrame:
    """
    Load data from a file path or a file-like object (e.g. uploaded file).
    Supports CSV and Excel files.
    """
    if isinstance(file_source, (str, Path)):
        # It's a path
        path = Path(file_source)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_source}")
        suffix = path.suffix.lower()
    else:
        # Streamlit UploadedFile object or file-like buffer
        name = getattr(file_source, "name", "")
        suffix = os.path.splitext(name)[1].lower() if name else ".csv"
    
    if suffix in [".csv", ".txt"]:
        # Try reading with default comma, fallback if needed
        try:
            if isinstance(file_source, (str, Path)):
                df = pd.read_csv(file_source)
            else:
                # Read content from buffer
                content = file_source.read()
                # If bytes, decode to string
                if isinstance(content, bytes):
                    # Try utf-8 first, fallback to latin-1
                    try:
                        decoded = content.decode('utf-8')
                    except UnicodeDecodeError:
                        decoded = content.decode('latin-1')
                else:
                    decoded = content
                
                # Sniff delimiter
                delim = ','
                first_line = decoded.split('\n')[0] if decoded else ""
                if ';' in first_line and first_line.count(';') > first_line.count(','):
                    delim = ';'
                elif '\t' in first_line:
                    delim = '\t'
                
                # Reset file-like seek if necessary, or load from decoded string
                df = pd.read_csv(io.StringIO(decoded), sep=delim)
        except Exception as e:
            raise ValueError(f"Error loading CSV file: {str(e)}")
            
    elif suffix in [".xlsx", ".xls"]:
        try:
            if isinstance(file_source, (str, Path)):
                df = pd.read_excel(file_source)
            else:
                # Seek to start
                if hasattr(file_source, "seek"):
                    file_source.seek(0)
                df = pd.read_excel(file_source)
        except Exception as e:
            raise ValueError(f"Error loading Excel file: {str(e)}")
    else:
        raise ValueError(f"Unsupported file format: {suffix}. Only CSV and Excel are supported.")
        
    # Standard cleanups: drop completely empty rows and columns
    df = df.dropna(how='all')
    
    return df

def validate_dataframe(df: pd.DataFrame) -> tuple[bool, list[str]]:
    """
    Perform structural validation checks on loaded dataframe.
    Returns (is_valid, error_messages)
    """
    errors = []
    if df.empty:
        errors.append("The uploaded dataset is empty.")
        return False, errors
        
    if len(df.columns) == 0:
        errors.append("The dataset has no columns.")
        
    # Unnamed columns check
    unnamed = [col for col in df.columns if "Unnamed:" in str(col)]
    if len(unnamed) == len(df.columns):
        errors.append("All columns in the dataset are unnamed.")
        
    return len(errors) == 0, errors
