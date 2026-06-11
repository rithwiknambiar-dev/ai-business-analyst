import streamlit as st
import pandas as pd

def format_number(val):
    """Format numeric values as currency, percentage, or clean float/int based on scale."""
    if val is None or pd.isna(val):
        return "N/A"
    
    # Check if integer
    if isinstance(val, (int, float)) and val == int(val):
        val = int(val)
        
    if isinstance(val, (int, float)):
        abs_val = abs(val)
        if abs_val >= 1_000_000_000:
            return f"{val / 1_000_000_000:.2f}B"
        elif abs_val >= 1_000_000:
            return f"{val / 1_000_000:.2f}M"
        elif abs_val >= 1_000:
            return f"{val:,.2f}" if isinstance(val, float) else f"{val:,}"
        elif abs_val < 1 and abs_val > 0:
            return f"{val:.4f}"
        else:
            return f"{val:.2f}" if isinstance(val, float) else f"{val}"
    return str(val)

def inject_premium_css():
    """Inject premium dark-mode css for Streamlit to style tables, metric cards, and dashboards."""
    st.markdown("""
        <style>
        /* Glassmorphism card style */
        .premium-card {
            background: rgba(25, 30, 40, 0.65);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(10px);
            margin-bottom: 15px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            transition: transform 0.2s ease, border-color 0.2s ease;
        }
        .premium-card:hover {
            transform: translateY(-2px);
            border-color: rgba(0, 229, 255, 0.3);
        }
        
        /* Metric labeling */
        .metric-title {
            font-size: 0.85rem;
            color: #8A99AD;
            text-transform: uppercase;
            letter-spacing: 1.2px;
            font-weight: 600;
            margin-bottom: 8px;
        }
        .metric-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: #FFFFFF;
            font-family: 'Outfit', 'Inter', sans-serif;
        }
        .metric-change {
            font-size: 0.9rem;
            font-weight: 500;
            margin-top: 4px;
        }
        .change-positive {
            color: #00E676;
        }
        .change-negative {
            color: #FF1744;
        }
        .change-neutral {
            color: #B0BEC5;
        }
        </style>
    """, unsafe_allow_html=True)

def render_metric_card(title, value, change=None, change_direction="up"):
    """Render a premium styled metric card with status indicators."""
    change_html = ""
    if change is not None:
        if change_direction == "up":
            change_html = f'<div class="metric-change change-positive">▲ {change}</div>'
        elif change_direction == "down":
            change_html = f'<div class="metric-change change-negative">▼ {change}</div>'
        else:
            change_html = f'<div class="metric-change change-neutral">● {change}</div>'
            
    st.markdown(f"""
        <div class="premium-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
            {change_html}
        </div>
    """, unsafe_allow_html=True)
