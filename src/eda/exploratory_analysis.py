import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def generate_correlation_matrix(df: pd.DataFrame):
    """
    Generate correlation matrix heatmap for all numeric columns.
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(numeric_cols) < 2:
        return None
        
    corr_df = df[numeric_cols].corr()
    
    fig = px.imshow(
        corr_df,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale="RdBu_r",
        title="Correlation Heatmap of Numeric Variables"
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFFFFF")
    )
    return fig

def generate_distribution_plot(df: pd.DataFrame, column: str, plot_type="histogram"):
    """
    Generate distribution plot (histogram or box plot) for a numeric column.
    """
    if column not in df.columns:
        return None
        
    if plot_type == "histogram":
        fig = px.histogram(
            df,
            x=column,
            marginal="box",
            title=f"Distribution of {column}",
            color_discrete_sequence=["#00E5FF"]
        )
    else:  # Box plot
        fig = px.box(
            df,
            y=column,
            title=f"Box Plot of {column}",
            color_discrete_sequence=["#D500F9"]
        )
        
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFFFFF")
    )
    return fig

def generate_categorical_bar(df: pd.DataFrame, category_col: str, count_col=None, agg_func="count"):
    """
    Generate category bar chart, optionally aggregating a numerical column.
    """
    if category_col not in df.columns:
        return None
        
    if count_col and count_col in df.columns:
        if agg_func == "sum":
            agg_df = df.groupby(category_col)[count_col].sum().reset_index()
            y_col = count_col
            title = f"Sum of {count_col} by {category_col}"
        elif agg_func == "mean":
            agg_df = df.groupby(category_col)[count_col].mean().reset_index()
            y_col = count_col
            title = f"Average of {count_col} by {category_col}"
        else:
            agg_df = df.groupby(category_col).size().reset_index(name="Count")
            y_col = "Count"
            title = f"Record Count by {category_col}"
    else:
        agg_df = df.groupby(category_col).size().reset_index(name="Count")
        y_col = "Count"
        title = f"Record Count by {category_col}"
        
    # Sort for cleaner visual representation
    agg_df = agg_df.sort_values(by=y_col, ascending=False).head(20)
    
    fig = px.bar(
        agg_df,
        x=category_col,
        y=y_col,
        title=title,
        color_discrete_sequence=["#2979FF"]
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFFFFF")
    )
    return fig

def generate_relationship_plot(df: pd.DataFrame, x_col: str, y_col: str, color_col=None, plot_type="scatter"):
    """
    Generate scatter or line relationship plot between x_col and y_col.
    """
    if x_col not in df.columns or y_col not in df.columns:
        return None
        
    if plot_type == "scatter":
        fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            color=color_col if color_col in df.columns else None,
            title=f"{y_col} vs {x_col}",
            color_continuous_scale="Viridis"
        )
    else:  # Line plot
        # For lines, check if we need to sort by x (especially useful if dates)
        sorted_df = df.sort_values(by=x_col)
        
        # If color column is present, group lines
        if color_col and color_col in df.columns:
            fig = px.line(
                sorted_df,
                x=x_col,
                y=y_col,
                color=color_col,
                title=f"{y_col} Trend over {x_col} by {color_col}"
            )
        else:
            fig = px.line(
                sorted_df,
                x=x_col,
                y=y_col,
                title=f"{y_col} Trend over {x_col}",
                color_discrete_sequence=["#FF9100"]
            )
            
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#FFFFFF")
    )
    return fig
