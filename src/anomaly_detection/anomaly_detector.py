import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

def detect_anomalies_zscore(df: pd.DataFrame, column: str, threshold=3.0) -> pd.DataFrame:
    """
    Detect statistical outliers using Z-score method.
    Returns a DataFrame containing anomalous rows.
    """
    if column not in df.columns or not pd.api.types.is_numeric_dtype(df[column]):
        return pd.DataFrame()
        
    series = df[column].dropna()
    if len(series) < 3:
        return pd.DataFrame()
        
    mean = series.mean()
    std = series.std()
    
    if std == 0:
        return pd.DataFrame()
        
    z_scores = (df[column] - mean) / std
    anomalies = df[np.abs(z_scores) > threshold].copy()
    anomalies["anomaly_score"] = z_scores[np.abs(z_scores) > threshold]
    anomalies["anomaly_reason"] = anomalies[column].apply(
        lambda x: f"Value ({x}) is {'above' if x > mean else 'below'} statistical bounds (Z-score = {((x-mean)/std):.2f})"
    )
    return anomalies

def detect_anomalies_multivariate(df: pd.DataFrame, columns: list[str], contamination=0.05) -> pd.DataFrame:
    """
    Detect multivariate anomalies using Isolation Forest.
    Returns a DataFrame containing anomalous rows.
    """
    valid_cols = [col for col in columns if col in df.columns and pd.api.types.is_numeric_dtype(df[col])]
    if len(valid_cols) == 0:
        return pd.DataFrame()
        
    # Drop rows with NaNs in target columns for fitting
    fit_df = df[valid_cols].dropna()
    if len(fit_df) < 5:
        return pd.DataFrame()
        
    iso = IsolationForest(contamination=contamination, random_state=42)
    predictions = iso.fit_predict(fit_df)
    scores = iso.decision_function(fit_df)
    
    # Map back to original dataframe indices
    anomaly_indices = fit_df.index[predictions == -1]
    
    anomalies = df.loc[anomaly_indices].copy()
    anomalies["anomaly_score"] = scores[predictions == -1]
    
    reasons = []
    for idx, row in anomalies.iterrows():
        # Find which column deviated the most from the mean
        max_dev_col = None
        max_dev = -1
        for col in valid_cols:
            mean_val = df[col].mean()
            std_val = df[col].std()
            if std_val > 0:
                dev = abs(row[col] - mean_val) / std_val
                if dev > max_dev:
                    max_dev = dev
                    max_dev_col = col
        if max_dev_col:
            reasons.append(f"Multivariate outlier. Primary driver: {max_dev_col} value {row[max_dev_col]} ({max_dev:.1f} std deviations from average)")
        else:
            reasons.append("Multivariate structural anomaly detected")
            
    anomalies["anomaly_reason"] = reasons
    return anomalies
