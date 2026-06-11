import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures

def generate_forecast(df: pd.DataFrame, date_col: str, target_col: str, horizon=6, freq='M') -> tuple[pd.DataFrame, str]:
    """
    Generate forecasts with confidence intervals using trend + seasonal features regression.
    Supports Monthly ('M'), Weekly ('W'), and Daily ('D') frequencies.
    Returns (forecast_df, status_message).
    """
    if date_col not in df.columns or target_col not in df.columns:
        return pd.DataFrame(), "Date or Target column missing from data."
        
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df = df.dropna(subset=[date_col, target_col])
    
    if len(df) < 5:
        return pd.DataFrame(), "Insufficient data points for forecasting (minimum 5 required)."
        
    # Group by date column with chosen frequency
    if freq == 'M':
        # Align to end of month
        grouped = df.groupby(pd.Grouper(key=date_col, freq='ME'))[target_col].sum().reset_index()
    elif freq == 'W':
        grouped = df.groupby(pd.Grouper(key=date_col, freq='W'))[target_col].sum().reset_index()
    else:
        grouped = df.groupby(pd.Grouper(key=date_col, freq='D'))[target_col].sum().reset_index()
        
    grouped = grouped.sort_values(date_col)
    
    if len(grouped) < 5:
        return pd.DataFrame(), "Insufficient aggregated data points for forecasting."
        
    # Define features: trend index and seasonality
    grouped['Trend'] = np.arange(len(grouped))
    
    # Simple seasonality based on month/week number
    if freq == 'M':
        grouped['Season'] = grouped[date_col].dt.month
    elif freq == 'W':
        grouped['Season'] = grouped[date_col].dt.isocalendar().week
    else:
        grouped['Season'] = grouped[date_col].dt.dayofweek
        
    # One-hot encode seasonality
    season_dummies = pd.get_dummies(grouped['Season'], prefix='season', drop_first=True)
    X = pd.concat([grouped[['Trend']], season_dummies], axis=1)
    y = grouped[target_col].values
    
    # Fit Ridge regression
    model = Ridge(alpha=1.0)
    model.fit(X, y)
    
    # Calculate residuals to estimate confidence interval standard deviation
    y_pred = model.predict(X)
    residuals = y - y_pred
    std_residual = np.std(residuals) if len(residuals) > 1 else 1.0
    
    # Generate future dates
    last_date = grouped[date_col].max()
    future_dates = []
    
    # Add periods according to frequency
    for i in range(1, horizon + 1):
        if freq == 'M':
            future_dates.append(last_date + pd.DateOffset(months=i))
        elif freq == 'W':
            future_dates.append(last_date + pd.DateOffset(weeks=i))
        else:
            future_dates.append(last_date + pd.DateOffset(days=i))
            
    future_df = pd.DataFrame({date_col: future_dates})
    # Ensure end-of-month alignment if monthly
    if freq == 'M':
         future_df[date_col] = future_df[date_col] + pd.offsets.MonthEnd(0)
         
    future_df['Trend'] = np.arange(len(grouped), len(grouped) + horizon)
    
    if freq == 'M':
        future_df['Season'] = future_df[date_col].dt.month
    elif freq == 'W':
        future_df['Season'] = future_df[date_col].dt.isocalendar().week
    else:
        future_df['Season'] = future_df[date_col].dt.dayofweek
        
    # Re-apply dummies matching original fit columns
    future_season_dummies = pd.get_dummies(future_df['Season'], prefix='season')
    # Align columns
    for col in season_dummies.columns:
        if col not in future_season_dummies.columns:
            future_season_dummies[col] = 0
    future_season_dummies = future_season_dummies[season_dummies.columns]
    
    X_future = pd.concat([future_df[['Trend']], future_season_dummies], axis=1)
    
    # Predict
    future_preds = model.predict(X_future)
    
    # Construct output dataframe
    history_df = pd.DataFrame({
        "Date": grouped[date_col],
        "Actual": grouped[target_col],
        "Forecast": y_pred,
        "Lower_CI": y_pred - (1.96 * std_residual),
        "Upper_CI": y_pred + (1.96 * std_residual),
        "Is_Forecast": False
    })
    
    # Lower bound shouldn't fall below zero if all actual values are non-negative
    if (y >= 0).all():
        history_df["Lower_CI"] = history_df["Lower_CI"].clip(lower=0)
        
    forecast_results = pd.DataFrame({
        "Date": future_df[date_col],
        "Actual": np.nan,
        "Forecast": future_preds,
        "Lower_CI": future_preds - (1.96 * std_residual),
        "Upper_CI": future_preds + (1.96 * std_residual),
        "Is_Forecast": True
    })
    
    if (y >= 0).all():
        forecast_results["Lower_CI"] = forecast_results["Lower_CI"].clip(lower=0)
        
    combined = pd.concat([history_df, forecast_results], ignore_index=True)
    return combined, "Forecast generated successfully."
