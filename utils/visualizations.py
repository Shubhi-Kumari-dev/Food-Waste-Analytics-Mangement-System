"""
Visualizations Module for Food Waste Analytics and Management System (Lab 7 & Lab 8).
Implements reusable plotting functions using Matplotlib, Seaborn, and Plotly:
- Lab 7: Line plots over time, Scatter plots with trendlines, Correlation Heatmaps
- Lab 8: Histograms, Box plots, Bar charts, Pie charts, Donut charts
- Charting libraries comparison matrix (Matplotlib vs Seaborn vs Plotly vs Excel)
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# Authentic Culinary & Food Management Color Palette (Warm spices, herbs, grains, and produce)
PALETTE = [
    '#EA580C',  # Saffron / Chili Orange (Warm, appetizing citrus & spice)
    '#16A34A',  # Fresh Herb / Basil Green (Fresh vegetables & sustainability)
    '#D97706',  # Golden Harvest / Rice & Grain Amber
    '#BE123C',  # Roasted Beet / Savory Crimson
    '#B45309',  # Toasted Bread Crust / Warm Earth
    '#0284C7',  # Cold Storage / Dairy Blue
    '#65A30D',  # Olive & Herb Green
    '#78350F'   # Roasted Cocoa / Espresso
]

# Food Category Specific Color Mapping for immediate recognition
CATEGORY_COLOR_MAP = {
    'Rice': '#F59E0B',         # Golden Saffron
    'Vegetables': '#16A34A',   # Garden Green
    'Bread': '#B45309',        # Toasted Wheat
    'Dairy': '#0284C7',        # Fresh Dairy Blue
    'Fruits': '#EA580C',       # Orchard Tangerine
    'Meat': '#BE123C',         # Roasted Crimson
    'Other': '#65A30D'         # Olive Herb
}

def _apply_modern_layout(fig, title="", height=410, theme_mode="light", show_title=False):
    """Applies a food-management styled typography and grid layout with Light/Dark support."""
    is_dark = (theme_mode == "dark")
    
    text_color = '#FDF5ED' if is_dark else '#2A1B10'
    sub_color = '#BFAFA2' if is_dark else '#6B5746'
    grid_color = 'rgba(255, 235, 215, 0.08)' if is_dark else '#EFE4D6'
    bg_color = 'rgba(0,0,0,0)'

    layout_kwargs = dict(
        font={'family': 'Plus Jakarta Sans, -apple-system, sans-serif', 'color': sub_color},
        plot_bgcolor=bg_color,
        paper_bgcolor=bg_color,
        hovermode="x unified",
        margin=dict(l=35, r=25, t=15 if not show_title else 50, b=55),
        height=height,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.16,
            xanchor="center",
            x=0.5,
            title_text="",
            font=dict(size=11, color=sub_color)
        )
    )

    if show_title and title:
        layout_kwargs['title'] = {
            'text': f"<b>{title}</b>",
            'font': {'family': 'Plus Jakarta Sans, -apple-system, sans-serif', 'size': 14, 'color': text_color},
            'x': 0.02,
            'y': 0.98,
            'xanchor': 'left',
            'yanchor': 'top'
        }
    else:
        layout_kwargs['title'] = dict(text="")

    fig.update_layout(**layout_kwargs)
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=grid_color, zeroline=False, tickfont=dict(color=sub_color))
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=grid_color, zeroline=False, tickfont=dict(color=sub_color))
    return fig

# ----------------- LAB 7: TEMPORAL TRENDS & CORRELATIONS ----------------- #

def plot_line_trend_by_group(df, group_col='Food_Category', date_freq='W', theme_mode="light"):
    """
    Lab 7.A: Line Plot analyzing food waste over time grouped by category or location.
    """
    if df.empty or 'Date' not in df.columns or 'Food_Wasted_Kg' not in df.columns:
        return go.Figure()

    temp_df = df.copy()
    temp_df['Date'] = pd.to_datetime(temp_df['Date'])
    
    # Resample and group
    grouped = temp_df.set_index('Date').groupby([pd.Grouper(freq=date_freq), group_col])['Food_Wasted_Kg'].sum().reset_index()

    fig = px.line(
        grouped,
        x='Date',
        y='Food_Wasted_Kg',
        color=group_col,
        markers=True,
        color_discrete_sequence=PALETTE,
        labels={'Food_Wasted_Kg': 'Food Wasted (kg)', 'Date': 'Date', group_col: ''}
    )
    fig.update_traces(line=dict(width=2.5), marker=dict(size=6))
    _apply_modern_layout(fig, title=f"Temporal Waste Trajectory by {group_col.replace('_', ' ')}", theme_mode=theme_mode)
    return fig

def plot_scatter_correlation(df, x_col='Food_Prepared_Kg', y_col='Food_Wasted_Kg', color_col='Food_Category', size_col=None, show_trendline=True, theme_mode="light"):
    """
    Lab 7.B: Scatter plot comparing two numeric variables with optional color/size grouping and OLS trendline.
    """
    if df.empty or x_col not in df.columns or y_col not in df.columns:
        return go.Figure(), 0.0

    corr_value = df[x_col].corr(df[y_col])
    trendline_type = "ols" if show_trendline else None
    valid_size = size_col if (size_col and size_col in df.columns and (df[size_col] > 0).all()) else None

    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color=color_col if (color_col and color_col in df.columns) else None,
        size=valid_size,
        trendline=trendline_type,
        color_discrete_sequence=PALETTE,
        labels={x_col: f"{x_col.replace('_', ' ')} (kg)", y_col: f"{y_col.replace('_', ' ')} (kg)"},
        hover_data=['Date', 'Location', 'Meal_Type'] if 'Date' in df.columns else None
    )
    is_dark = (theme_mode == "dark")
    border_col = '#3D2D22' if is_dark else '#FFFFFF'
    fig.update_traces(marker=dict(opacity=0.85, line=dict(width=0.8, color=border_col)))
    _apply_modern_layout(fig, title=f"Correlation Scatter: {x_col.replace('_', ' ')} vs {y_col.replace('_', ' ')} (r = {corr_value:.3f})", theme_mode=theme_mode)
    return fig, corr_value

def plot_correlation_heatmap_seaborn(df, theme_mode="light"):
    """
    Generates a Seaborn Correlation Heatmap for numeric columns with warm culinary aesthetics (Lab 7).
    """
    numeric_df = df.select_dtypes(include=[np.number])
    cols_to_corr = [c for c in ['Food_Prepared_Kg', 'Food_Served_Kg', 'Food_Wasted_Kg'] if c in numeric_df.columns]

    is_dark = (theme_mode == "dark")
    bg_color = '#221B16' if is_dark else '#FFFFFF'
    text_color = '#FDF5ED' if is_dark else '#2A1B10'
    line_color = '#3D2D22' if is_dark else '#FFFFFF'

    fig, ax = plt.subplots(figsize=(6, 3.8), dpi=120)
    fig.patch.set_facecolor(bg_color)
    ax.set_facecolor(bg_color)

    if len(cols_to_corr) > 1:
        corr_matrix = numeric_df[cols_to_corr].corr()
        sns.heatmap(
            corr_matrix,
            annot=True,
            cmap='YlOrBr',
            fmt=".3f",
            linewidths=1.5,
            linecolor=line_color,
            cbar=True,
            ax=ax,
            annot_kws={'size': 11, 'weight': 'bold', 'color': text_color}
        )
        ax.set_title("Pearson Correlation Matrix", fontsize=12, weight='bold', pad=10, color=text_color)
        ax.set_xticklabels([c.replace('_', ' ') for c in cols_to_corr], fontsize=9, rotation=15, color=text_color)
        ax.set_yticklabels([c.replace('_', ' ') for c in cols_to_corr], fontsize=9, rotation=0, color=text_color)
        cbar = ax.collections[0].colorbar
        cbar.ax.yaxis.set_tick_params(color=text_color)
        plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color=text_color)
    else:
        ax.text(0.5, 0.5, "Insufficient numeric columns", ha='center', va='center', color=text_color)

    plt.tight_layout()
    return fig

# ----------------- LAB 8: DISTRIBUTIONS & CATEGORICAL CHARTS ----------------- #

def plot_histogram(df, column='Food_Wasted_Kg', bins=20, color_group=None, theme_mode="light"):
    """
    Lab 8.A: Histogram showing the distribution of waste quantities with adjustable bins.
    """
    if df.empty or column not in df.columns:
        return go.Figure()

    fig = px.histogram(
        df,
        x=column,
        color=color_group if color_group and color_group != 'None' else None,
        nbins=bins,
        marginal="box",
        color_discrete_sequence=PALETTE,
        labels={column: f"{column.replace('_', ' ')} (kg)", 'count': 'Frequency (Observations)'},
        opacity=0.85
    )
    _apply_modern_layout(fig, title=f"Distribution of {column.replace('_', ' ')} (Bins = {bins})", theme_mode=theme_mode)
    return fig

def plot_boxplot(df, y_col='Food_Wasted_Kg', x_col='Food_Category', theme_mode="light"):
    """
    Lab 8.B: Box-and-Whisker plot displaying waste distribution and identifying potential outliers.
    """
    if df.empty or y_col not in df.columns:
        return go.Figure()

    fig = px.box(
        df,
        x=x_col if x_col in df.columns else None,
        y=y_col,
        color=x_col if x_col in df.columns else None,
        points="outliers",
        color_discrete_sequence=PALETTE,
        labels={y_col: f"{y_col.replace('_', ' ')} (kg)", x_col: x_col.replace('_', ' ')}
    )
    _apply_modern_layout(fig, title=f"Distribution & Outlier Profiler: {y_col.replace('_', ' ')} by {x_col.replace('_', ' ')}", theme_mode=theme_mode)
    return fig

def plot_barchart_aggregate(df, group_col='Food_Category', metric='sum', theme_mode="light"):
    """
    Lab 8.C: Bar chart comparing total or average waste across categorical variables.
    """
    if df.empty or group_col not in df.columns or 'Food_Wasted_Kg' not in df.columns:
        return go.Figure()

    if metric == 'sum':
        agg_df = df.groupby(group_col)['Food_Wasted_Kg'].sum().reset_index()
        title_metric = "Total Waste (kg)"
    else:
        agg_df = df.groupby(group_col)['Food_Wasted_Kg'].mean().reset_index()
        title_metric = "Average Waste (kg)"

    agg_df = agg_df.sort_values(by='Food_Wasted_Kg', ascending=False)

    fig = px.bar(
        agg_df,
        x=group_col,
        y='Food_Wasted_Kg',
        color='Food_Wasted_Kg',
        color_continuous_scale='Oranges',
        text_auto='.1f',
        labels={'Food_Wasted_Kg': title_metric, group_col: group_col.replace('_', ' ')}
    )
    fig.update_layout(coloraxis_showscale=False)
    _apply_modern_layout(fig, title=f"{title_metric} across {group_col.replace('_', ' ')}", theme_mode=theme_mode)
    return fig

def plot_pie_and_donut_chart(df, group_col='Waste_Cause', is_donut=True, theme_mode="light"):
    """
    Lab 8.D & 8.E: Pie and Donut chart displaying proportional contributions.
    """
    if df.empty or group_col not in df.columns or 'Food_Wasted_Kg' not in df.columns:
        return go.Figure()

    agg_df = df.groupby(group_col)['Food_Wasted_Kg'].sum().reset_index()
    hole_size = 0.50 if is_donut else 0.0
    chart_type = "Donut Chart" if is_donut else "Pie Chart"
    is_dark = (theme_mode == "dark")
    border_color = '#221B16' if is_dark else '#FFFFFF'

    fig = px.pie(
        agg_df,
        names=group_col,
        values='Food_Wasted_Kg',
        hole=hole_size,
        color_discrete_sequence=PALETTE
    )
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        marker=dict(line=dict(color=border_color, width=2))
    )
    _apply_modern_layout(fig, title=f"{chart_type}: Proportions by {group_col.replace('_', ' ')}", theme_mode=theme_mode)
    fig.update_layout(showlegend=False)
    return fig

# ----------------- LAB 8.F: COMPARISON OF CHARTING TOOLS ----------------- #

def get_chart_tools_comparison_df():
    """
    Returns a structured comparison table evaluating Matplotlib, Seaborn, Plotly, and Excel
    across Usability, Flexibility, Interactivity, and Visual Appearance.
    """
    data = [
        {
            "Tool": "Matplotlib",
            "Usability": "Moderate (Object-oriented & procedural syntax)",
            "Flexibility": "Extremely High (Pixel-level fine control of canvas)",
            "Interactivity": "Low (Static raster/vector outputs)",
            "Visual Appearance": "Academic / Formal (Clean publication figures)",
            "Ideal Scenario": "Research papers, academic submissions, thesis figures"
        },
        {
            "Tool": "Seaborn",
            "Usability": "High (Declarative high-level statistical syntax)",
            "Flexibility": "High (Built on Matplotlib; exposes statistical fits)",
            "Interactivity": "Low (Generates static matplotlib figures)",
            "Visual Appearance": "Modern Statistical (Polished color themes & KDEs)",
            "Ideal Scenario": "Exploratory Data Analysis (EDA), regression lines, heatmaps"
        },
        {
            "Tool": "Plotly",
            "Usability": "Very High (Express API with intuitive arguments)",
            "Flexibility": "High (Graph Objects allows custom layering)",
            "Interactivity": "Very High (Native browser zoom, pan, hover tooltips)",
            "Visual Appearance": "Executive & Web-Ready (Sleek reactive animations)",
            "Ideal Scenario": "Interactive dashboards (Streamlit), client presentations"
        },
        {
            "Tool": "Microsoft Excel",
            "Usability": "Very High (Point-and-click GUI; universal adoption)",
            "Flexibility": "Moderate (Restricted to predefined chart templates)",
            "Interactivity": "Moderate (Slicers, PivotCharts, timeline filters)",
            "Visual Appearance": "Standard Corporate (Familiar office look)",
            "Ideal Scenario": "Ad-hoc business reporting, quick pivot summaries, auditing"
        }
    ]
    return pd.DataFrame(data)
