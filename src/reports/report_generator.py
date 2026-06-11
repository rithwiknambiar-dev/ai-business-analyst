import datetime

def generate_html_report(dataset_name: str, profile_summary: dict, insights: list[dict], anomalies_df=None) -> str:
    """
    Build a polished, print-ready HTML/CSS business intelligence report.
    Returns the raw HTML string.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Format Insights
    insights_html = ""
    for ins in insights:
        bg_color = "#E1F5FE"
        border_color = "#03A9F4"
        text_color = "#01579B"
        
        if ins["type"] == "warning":
            bg_color = "#FFEBEE"
            border_color = "#EF5350"
            text_color = "#C62828"
        elif ins["type"] == "success":
            bg_color = "#E8F5E9"
            border_color = "#66BB6A"
            text_color = "#2E7D32"
            
        insights_html += f"""
        <div style="background-color: {bg_color}; border-left: 5px solid {border_color}; color: {text_color}; padding: 15px; margin-bottom: 12px; border-radius: 4px; font-family: sans-serif;">
            <strong style="font-size: 1.1em; display: block; margin-bottom: 5px;">{ins['title']}</strong>
            <span>{ins['description']}</span>
        </div>
        """
        
    # Format Anomalies
    anomalies_html = ""
    if anomalies_df is not None and not anomalies_df.empty:
        rows = ""
        # Get first 15 anomalies to avoid huge tables
        for idx, row in anomalies_df.head(15).iterrows():
            reason = row.get("anomaly_reason", "Statistical Outlier")
            rows += f"""
            <tr style="border-bottom: 1px solid #ddd;">
                <td style="padding: 10px; text-align: left; font-family: monospace;">Row {idx + 1}</td>
                <td style="padding: 10px; text-align: left; color: #d32f2f;">{reason}</td>
            </tr>
            """
        anomalies_html = f"""
        <div style="margin-top: 30px;">
            <h3 style="color: #d32f2f; font-family: sans-serif; border-bottom: 2px solid #d32f2f; padding-bottom: 8px;">Key Flagged Anomalies</h3>
            <table style="width: 100%; border-collapse: collapse; margin-top: 10px; font-family: sans-serif; font-size: 0.95em;">
                <thead>
                    <tr style="background-color: #f5f5f5; border-bottom: 2px solid #ddd;">
                        <th style="padding: 12px 10px; text-align: left;">Record Index</th>
                        <th style="padding: 12px 10px; text-align: left;">Reason / Driver</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
        """
    else:
        anomalies_html = """
        <div style="margin-top: 30px; background-color: #E8F5E9; border-left: 5px solid #2E7D32; color: #2E7D32; padding: 15px; border-radius: 4px; font-family: sans-serif;">
            <strong>No major anomalies detected.</strong> All records reside within normal statistical bounds.
        </div>
        """
        
    # Master Template
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>BI Analyst Executive Report - {dataset_name}</title>
        <style>
            body {{
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                color: #333333;
                background-color: #ffffff;
                line-height: 1.6;
                padding: 40px;
                margin: 0;
            }}
            .header {{
                border-bottom: 3px solid #2c3e50;
                padding-bottom: 20px;
                margin-bottom: 30px;
            }}
            .header h1 {{
                margin: 0;
                font-size: 2.2em;
                color: #2c3e50;
            }}
            .meta {{
                font-size: 0.9em;
                color: #7f8c8d;
                margin-top: 5px;
            }}
            .stats-container {{
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 15px;
                margin-bottom: 35px;
            }}
            .stat-card {{
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                padding: 15px;
                border-radius: 6px;
                text-align: center;
            }}
            .stat-title {{
                font-size: 0.85em;
                color: #6c757d;
                text-transform: uppercase;
                letter-spacing: 0.8px;
                margin-bottom: 5px;
            }}
            .stat-val {{
                font-size: 1.6em;
                font-weight: bold;
                color: #2c3e50;
            }}
            .section-title {{
                color: #2c3e50;
                font-family: sans-serif;
                border-bottom: 2px solid #2c3e50;
                padding-bottom: 8px;
                margin-top: 40px;
                margin-bottom: 20px;
            }}
            .footer {{
                margin-top: 60px;
                border-top: 1px solid #e2e8f0;
                padding-top: 15px;
                text-align: center;
                font-size: 0.85em;
                color: #a0aec0;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Executive Summary Report</h1>
            <div class="meta">Dataset: <strong>{dataset_name}</strong> | Generated on: {timestamp}</div>
        </div>
        
        <div class="stats-container">
            <div class="stat-card">
                <div class="stat-title">Total Records</div>
                <div class="stat-val">{profile_summary.get('num_rows', 0):,}</div>
            </div>
            <div class="stat-card">
                <div class="stat-title">Dimensions</div>
                <div class="stat-val">{profile_summary.get('num_cols', 0)}</div>
            </div>
            <div class="stat-card">
                <div class="stat-title">Missing Ratio</div>
                <div class="stat-val">{profile_summary.get('overall_missing_pct', 0.0):.1f}%</div>
            </div>
            <div class="stat-card">
                <div class="stat-title">Data Quality Score</div>
                <div class="stat-val">{profile_summary.get('data_quality_score', 100.0)}/100</div>
            </div>
        </div>
        
        <h2 class="section-title">Automated Business Insights</h2>
        <div>
            {insights_html}
        </div>
        
        {anomalies_html}
        
        <div class="footer">
            Generated automatically by Antigravity AI Business Analyst System
        </div>
    </body>
    </html>
    """
    
    return html_template
