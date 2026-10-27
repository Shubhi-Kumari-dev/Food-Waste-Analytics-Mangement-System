"""
Food Waste Analytics and Management System
Executive Web Application for Data Analytics & Visualization Lab.
Built with Streamlit, Pandas, NumPy, Matplotlib, Seaborn, Plotly, SQLAlchemy, and Statsmodels.
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime

# Modular utility functions
from utils.data_processing import (
    load_data_file,
    validate_columns,
    get_data_quality_report,
    clean_food_waste_data,
    calculate_kpis,
    convert_df_to_csv,
    REQUIRED_COLUMNS
)
from utils.database import (
    get_record_count,
    save_data_to_db,
    run_custom_query,
    insert_kitchen_log_entry,
    DB_FILE,
    TABLE_NAME
)
from utils.visualizations import (
    plot_line_trend_by_group,
    plot_scatter_correlation,
    plot_correlation_heatmap_seaborn,
    plot_histogram,
    plot_boxplot,
    plot_barchart_aggregate,
    plot_pie_and_donut_chart,
    get_chart_tools_comparison_df
)
from utils.time_series import (
    prepare_time_series,
    plot_trend_and_moving_average,
    compute_exponential_smoothing,
    compute_seasonal_decomposition,
    run_arima_forecast
)
from utils.recommendations import (
    run_regression_analysis,
    generate_waste_reduction_insights,
    simulate_waste_reduction
)

# ----------------- PAGE CONFIGURATION ----------------- #
st.set_page_config(
    page_title="Food Waste Analytics & Management System",
    page_icon="🍲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- BACKEND AUTOMATED PIPELINE ----------------- #
DEFAULT_CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "food_waste_sample.csv")

def execute_backend_pipeline(raw_df, source_label="Sample Repository"):
    """
    Automated ETL Pipeline:
    Cleans, validates bounds, imputes missing values, and synchronizes to SQLite.
    Runs silently in the background.
    """
    cleaned_df, log = clean_food_waste_data(raw_df, handle_missing="mean_mode", remove_duplicates=True)
    save_data_to_db(cleaned_df, mode="replace")
    
    st.session_state.active_df = cleaned_df
    st.session_state.cleaning_log = log
    st.session_state.dataset_source = source_label
    return cleaned_df

# Startup: Auto-load dataset into memory & database if not present
if 'active_df' not in st.session_state or st.session_state.active_df is None:
    if os.path.exists(DEFAULT_CSV_PATH):
        sample_raw = pd.read_csv(DEFAULT_CSV_PATH)
        execute_backend_pipeline(sample_raw, "Verified Baseline Dataset (420 records)")
    else:
        st.session_state.active_df = None
        st.session_state.cleaning_log = []
        st.session_state.dataset_source = "None"

# ----------------- THEME TOGGLE & CULINARY PALETTE SELECTION ----------------- #
# Theme switcher in sidebar
with st.sidebar:
    st.markdown("""
    <div style="font-size:0.75rem; font-weight:700; text-transform:uppercase; letter-spacing:0.05em; color:#9C8573; margin-bottom:4px;">
        Dining Atmosphere
    </div>
    """, unsafe_allow_html=True)
    theme_choice = st.radio(
        "Dining Atmosphere:",
        ["☀️ Warm Bistro (Light)", "🌙 Midnight Roast (Dark)"],
        index=0,
        horizontal=True,
        label_visibility="collapsed",
        key="app_dining_theme"
    )

is_dark = ("Dark" in theme_choice)
theme_mode = "dark" if is_dark else "light"

# ----------------- DYNAMIC CULINARY FOOD STYLING (CSS) ----------------- #
if is_dark:
    # Deep Roasted Espresso / Charcoal Bistro Dark Theme
    c_canvas = "#14100D"
    c_sidebar = "#1B1511"
    c_card = "#221A15"
    c_border = "#3D2D22"
    c_text_main = "#FDF5ED"
    c_text_muted = "#BFAFA2"
    c_text_dim = "#8F7D70"
    c_accent_saffron = "#F97316"
    c_accent_green = "#22C55E"
    c_accent_amber = "#FBBF24"
    c_accent_crimson = "#EF4444"
    c_accent_cinnamon = "#D97706"
    c_shadow = "0 4px 18px rgba(0, 0, 0, 0.45)"
    c_tag_bg = "#2C2018"
    c_tag_border = "#4A3525"
    c_banner_bg = "linear-gradient(135deg, #221A15 0%, #1A130E 100%)"
    c_rec_banner_bg = "linear-gradient(135deg, #3A170A 0%, #4D1E0C 50%, #7C2D12 100%)"
    c_rec_tag_color = "#FED7AA"
    c_rec_sub_color = "#FFEDD5"
    c_alert_bg = "#2A1D13"
    c_alert_border = "#F97316"
    c_alert_text = "#FED7AA"
    c_table_bg = "#1B1511"
else:
    # Warm Soft Cream Ivory / Fresh Kitchen Light Theme
    c_canvas = "#FDFBF7"
    c_sidebar = "#F7F1E7"
    c_card = "#FFFFFF"
    c_border = "#EBDDCF"
    c_text_main = "#2A1B10"
    c_text_muted = "#6B5746"
    c_text_dim = "#9C8573"
    c_accent_saffron = "#EA580C"
    c_accent_green = "#16A34A"
    c_accent_amber = "#D97706"
    c_accent_crimson = "#DC2626"
    c_accent_cinnamon = "#B45309"
    c_shadow = "0 2px 10px rgba(180, 83, 9, 0.05)"
    c_tag_bg = "#FFF7ED"
    c_tag_border = "#FED7AA"
    c_banner_bg = "linear-gradient(135deg, #FFFFFF 0%, #FAF6EE 100%)"
    c_rec_banner_bg = "linear-gradient(135deg, #7C2D12 0%, #9A3412 50%, #C2410C 100%)"
    c_rec_tag_color = "#FED7AA"
    c_rec_sub_color = "#FFEDD5"
    c_alert_bg = "#FFF8EE"
    c_alert_border = "#FDBA74"
    c_alert_text = "#9A3412"
    c_table_bg = "#FFFFFF"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    /* Universal Font and Canvas */
    html, body, [class*="css"], .stApp {{
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        background-color: {c_canvas} !important;
        color: {c_text_main} !important;
    }}

    /* Sidebar Background & Borders */
    section[data-testid="stSidebar"] {{
        background-color: {c_sidebar} !important;
        border-right: 1px solid {c_border} !important;
    }}
    section[data-testid="stSidebar"] * {{
        color: {c_text_main};
    }}

    /* Brand Header Box */
    .app-brand-banner {{
        background: {c_banner_bg};
        border: 1px solid {c_border};
        border-radius: 16px;
        padding: 1.35rem 1.75rem;
        margin-bottom: 1.15rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1.2rem;
        box-shadow: {c_shadow};
        position: relative;
        overflow: hidden;
    }}
    .app-brand-banner::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, {c_accent_saffron} 0%, {c_accent_amber} 50%, {c_accent_cinnamon} 100%);
    }}
    .app-brand-badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: {c_tag_bg};
        border: 1px solid {c_tag_border};
        color: {c_accent_saffron};
        font-size: 0.69rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        padding: 3px 11px;
        border-radius: 20px;
        margin-bottom: 0.45rem;
    }}
    .app-brand-title {{
        font-size: 1.62rem;
        font-weight: 800;
        color: {c_text_main};
        letter-spacing: -0.025em;
        display: flex;
        align-items: center;
        gap: 0.65rem;
        line-height: 1.2;
    }}
    .app-brand-subtitle {{
        font-size: 0.86rem;
        color: {c_text_muted};
        margin-top: 0.3rem;
        font-weight: 500;
        max-width: 820px;
    }}
    .kitchen-status-pill {{
        background: {c_tag_bg};
        border: 1px solid {c_tag_border};
        color: {c_accent_saffron};
        font-size: 0.8rem;
        font-weight: 700;
        padding: 6px 14px;
        border-radius: 30px;
        display: inline-flex;
        align-items: center;
        gap: 7px;
    }}
    .header-badges-wrap {{
        display: flex;
        align-items: center;
        gap: 0.55rem;
        flex-wrap: wrap;
    }}
    .header-info-chip {{
        background: {c_card};
        border: 1px solid {c_border};
        color: {c_text_muted};
        font-size: 0.78rem;
        font-weight: 600;
        padding: 6px 12px;
        border-radius: 20px;
        display: inline-flex;
        align-items: center;
        gap: 5px;
        box-shadow: 0 1px 4px rgba(0,0,0,0.03);
    }}

    /* Filter Panel Container Styling */
    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background: {c_card} !important;
        border: 1px solid {c_border} !important;
        border-radius: 14px !important;
        box-shadow: {c_shadow} !important;
        margin-bottom: 1.15rem !important;
    }}

    /* KPI Summary Cards Grid - Guaranteed 5 Cards on Single Row on Desktop/Laptop */
    .kpi-deck {{
        display: grid;
        grid-template-columns: repeat(5, minmax(0, 1fr));
        gap: 0.75rem;
        margin-bottom: 1.25rem;
    }}
    @media (max-width: 860px) {{
        .kpi-deck {{
            grid-template-columns: repeat(3, minmax(0, 1fr));
        }}
    }}
    @media (max-width: 580px) {{
        .kpi-deck {{
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }}
    }}

    /* KPI Plate with Luxury Glassmorphism & Accent Top Ribbon */
    .kpi-plate {{
        background: {c_card};
        border: 1px solid {c_border};
        border-radius: 14px;
        padding: 1.1rem 1rem 0.95rem 1rem;
        box-shadow: {c_shadow};
        position: relative;
        overflow: hidden;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        min-height: 122px;
    }}
    .kpi-plate:hover {{
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(180, 83, 9, 0.12);
    }}
    .kpi-accent-ribbon {{
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        border-radius: 14px 14px 0 0;
    }}
    .kpi-top-bar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.35rem;
    }}
    .kpi-plate-title {{
        font-size: 0.70rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: {c_text_muted};
        display: flex;
        align-items: center;
        gap: 0.35rem;
    }}
    .kpi-badge-pill {{
        font-size: 0.65rem;
        font-weight: 700;
        padding: 2px 7px;
        border-radius: 6px;
        white-space: nowrap;
    }}
    .kpi-plate-val {{
        font-size: 1.60rem;
        font-weight: 800;
        color: {c_text_main};
        margin: 0.25rem 0 0.15rem 0;
        line-height: 1.15;
    }}
    .kpi-plate-unit {{
        font-size: 0.85rem;
        font-weight: 600;
        color: {c_text_muted};
    }}
    .kpi-plate-sub {{
        font-size: 0.73rem;
        color: {c_text_dim};
        font-weight: 500;
        line-height: 1.35;
    }}

    /* Action Recommendations Callout Banner */
    .action-cta-card {{
        background: {c_card};
        border: 1px solid {c_border};
        border-left: 5px solid {c_accent_saffron};
        border-radius: 14px;
        padding: 1rem 1.4rem;
        margin-bottom: 1.25rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1rem;
        box-shadow: {c_shadow};
        transition: transform 0.15s ease;
    }}
    .action-cta-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(234, 88, 12, 0.15);
    }}

    /* Data-Backed Recommendations Hero Banner - Warm Bistro Spiced Theme (NO GREEN) */
    .rec-hero-banner {{
        background: {c_rec_banner_bg};
        border-radius: 14px;
        padding: 1.4rem 1.8rem;
        margin-bottom: 1.15rem;
        color: #FFFFFF;
        box-shadow: 0 6px 20px rgba(124, 45, 18, 0.22);
    }}
    .rec-hero-tag {{
        display: inline-block;
        background: rgba(255, 255, 255, 0.18);
        border: 1px solid rgba(255, 255, 255, 0.35);
        color: {c_rec_tag_color};
        font-size: 0.69rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        padding: 3px 10px;
        border-radius: 20px;
        margin-bottom: 0.45rem;
    }}
    .rec-hero-title {{
        font-size: 1.62rem;
        font-weight: 800;
        color: #FFFFFF;
        margin-bottom: 0.3rem;
        line-height: 1.2;
    }}
    .rec-hero-sub {{
        font-size: 0.86rem;
        color: {c_rec_sub_color};
        max-width: 860px;
        line-height: 1.45;
        margin-bottom: 0.85rem;
    }}
    .rec-hero-pills {{
        display: flex;
        gap: 0.55rem;
        flex-wrap: wrap;
    }}
    .rec-hero-pill {{
        background: rgba(255, 255, 255, 0.14);
        border: 1px solid rgba(255, 255, 255, 0.28);
        color: #FFFFFF;
        font-size: 0.76rem;
        font-weight: 600;
        padding: 4px 12px;
        border-radius: 20px;
    }}

    /* Prioritized Protocol Cards - Warm Theme (NO GREEN) */
    .protocol-card {{
        background: {c_card};
        border: 1px solid {c_border};
        border-radius: 12px;
        padding: 1.15rem 1.35rem;
        margin-bottom: 0.95rem;
        box-shadow: {c_shadow};
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }}
    .protocol-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 6px 18px rgba(180, 83, 9, 0.12);
    }}
    .protocol-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 0.8rem;
        margin-bottom: 0.35rem;
    }}
    .protocol-title-wrap {{
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }}
    .protocol-title {{
        font-size: 1.05rem;
        font-weight: 700;
        color: {c_text_main};
    }}
    .protocol-focus {{
        font-size: 0.80rem;
        font-weight: 600;
        color: {c_text_dim};
        margin-bottom: 0.4rem;
    }}
    .protocol-finding {{
        font-size: 0.86rem;
        color: {c_text_muted};
        margin-bottom: 0.75rem;
        line-height: 1.45;
    }}
    .protocol-action-box {{
        background: {c_tag_bg};
        border: 1px solid {c_tag_border};
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 0.6rem;
    }}
    .protocol-action-label {{
        font-size: 0.70rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: {c_accent_saffron};
        margin-bottom: 3px;
    }}
    .protocol-action-text {{
        font-size: 0.88rem;
        font-weight: 600;
        color: {c_text_main};
        line-height: 1.4;
    }}
    .protocol-followup {{
        font-size: 0.80rem;
        color: {c_text_dim};
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }}
    .priority-badge-high {{
        background: rgba(220, 38, 38, 0.12);
        color: #DC2626;
        border: 1px solid rgba(220, 38, 38, 0.3);
        font-weight: 700;
        font-size: 0.74rem;
        padding: 3px 10px;
        border-radius: 20px;
        white-space: nowrap;
    }}
    .priority-badge-medium {{
        background: rgba(234, 88, 12, 0.12);
        color: #EA580C;
        border: 1px solid rgba(234, 88, 12, 0.3);
        font-weight: 700;
        font-size: 0.74rem;
        padding: 3px 10px;
        border-radius: 20px;
        white-space: nowrap;
    }}
    .priority-badge-low {{
        background: rgba(217, 119, 6, 0.12);
        color: #D97706;
        border: 1px solid rgba(217, 119, 6, 0.3);
        font-weight: 700;
        font-size: 0.74rem;
        padding: 3px 10px;
        border-radius: 20px;
        white-space: nowrap;
    }}

    /* Workflow Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 6px;
        background-color: {c_card};
        padding: 6px;
        border-radius: 12px;
        border: 1px solid {c_border};
        margin-bottom: 1.2rem;
        box-shadow: {c_shadow};
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 600;
        font-size: 0.88rem;
        color: {c_text_muted} !important;
        background: transparent;
        border: none;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: {c_sidebar} !important;
        color: {c_accent_saffron} !important;
        font-weight: 700 !important;
        border: 1px solid {c_accent_saffron} !important;
    }}

    /* Segmented Control Styled as Modern Luxury Tabs */
    div[data-testid="stSegmentedControl"] {{
        background-color: {c_card} !important;
        padding: 5px !important;
        border-radius: 14px !important;
        border: 1px solid {c_border} !important;
        margin-bottom: 1.25rem !important;
        box-shadow: {c_shadow} !important;
    }}
    div[data-testid="stSegmentedControl"] button {{
        border-radius: 9px !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        color: {c_text_muted} !important;
        border: none !important;
        padding: 8px 16px !important;
        transition: all 0.15s ease !important;
    }}
    div[data-testid="stSegmentedControl"] button:hover {{
        background: {c_tag_bg} !important;
        color: {c_text_main} !important;
    }}
    div[data-testid="stSegmentedControl"] button[aria-checked="true"] {{
        background-color: {c_sidebar} !important;
        color: {c_accent_saffron} !important;
        font-weight: 700 !important;
        border: 1px solid {c_accent_saffron} !important;
        box-shadow: 0 2px 8px rgba(234, 88, 12, 0.15) !important;
    }}

    /* Structured Chart Box Titles */
    .chart-panel-title {{
        font-size: 0.98rem;
        font-weight: 700;
        color: {c_text_main};
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}

    /* Sidebar Styled Components */
    .sidebar-brand-box {{
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 0.4rem 0 0.8rem 0;
        margin-bottom: 0.6rem;
        border-bottom: 1px solid {c_border};
    }}
    .sidebar-brand-icon {{
        font-size: 1.7rem;
        background: {c_tag_bg};
        border: 1px solid {c_tag_border};
        border-radius: 10px;
        padding: 4px 8px;
    }}
    .sidebar-brand-title {{
        font-size: 1.15rem;
        font-weight: 800;
        color: {c_text_main};
        line-height: 1.15;
    }}
    .sidebar-brand-sub {{
        font-size: 0.73rem;
        color: {c_text_muted};
    }}

    /* Telemetry Live Badge */
    .telemetry-card {{
        background: {c_card};
        border: 1px solid {c_border};
        border-radius: 10px;
        padding: 10px 12px;
        margin-bottom: 14px;
        box-shadow: {c_shadow};
    }}
    .telemetry-pill {{
        font-size: 0.70rem;
        font-weight: 700;
        text-transform: uppercase;
        color: {c_accent_green};
        display: flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 3px;
    }}
    .telemetry-num {{
        font-size: 1.12rem;
        font-weight: 800;
        color: {c_text_main};
    }}
    .telemetry-sub {{
        font-size: 0.71rem;
        color: {c_text_dim};
    }}
    .pulse-dot {{
        width: 7px;
        height: 7px;
        background-color: {c_accent_green};
        border-radius: 50%;
        display: inline-block;
        box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7);
        animation: pulse 1.6s infinite;
    }}
    @keyframes pulse {{
        0% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0.7); }}
        70% {{ transform: scale(1); box-shadow: 0 0 0 6px rgba(34, 197, 94, 0); }}
        100% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(34, 197, 94, 0); }}
    }}

    /* Facility Cards (Replacing plain bullets) */
    .facility-list-wrap {{
        display: flex;
        flex-direction: column;
        gap: 7px;
        margin: 8px 0 14px 0;
    }}
    .facility-item {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: {c_card};
        border: 1px solid {c_border};
        border-radius: 9px;
        padding: 7px 10px;
        transition: transform 0.15s ease;
    }}
    .facility-item:hover {{
        transform: translateX(2px);
    }}
    .fac-left {{
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    .fac-name {{
        font-size: 0.82rem;
        font-weight: 700;
        color: {c_text_main};
        line-height: 1.15;
    }}
    .fac-desc {{
        font-size: 0.69rem;
        color: {c_text_dim};
    }}
    .fac-pill {{
        font-size: 0.68rem;
        font-weight: 700;
        padding: 2px 7px;
        border-radius: 6px;
        background: {c_tag_bg};
        border: 1px solid {c_tag_border};
        color: {c_accent_saffron};
    }}

    .section-header-styled {{
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        color: {c_text_muted};
        margin-top: 10px;
        margin-bottom: 6px;
    }}

    /* Card Content Title */
    .chart-panel-title {{
        font-size: 1.05rem;
        font-weight: 700;
        color: {c_text_main};
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.45rem;
    }}

    /* Clean Streamlit Widgets */
    header[data-testid="stHeader"] {{
        background-color: transparent !important;
    }}
    div[data-testid="stMetric"] {{
        background: {c_card} !important;
        border: 1px solid {c_border} !important;
        border-radius: 10px !important;
        padding: 12px !important;
    }}
    button[kind="primary"] {{
        background: linear-gradient(135deg, {c_accent_saffron} 0%, {c_accent_amber} 100%) !important;
        border: none !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }}
    button[kind="secondary"] {{
        background: {c_card} !important;
        border: 1px solid {c_border} !important;
        color: {c_text_main} !important;
        font-weight: 600 !important;
    }}
    div[data-testid="stExpander"] {{
        background: {c_card} !important;
        border: 1px solid {c_border} !important;
        border-radius: 12px !important;
    }}
</style>
""", unsafe_allow_html=True)

# ----------------- REFINED CULINARY SIDEBAR ----------------- #
with st.sidebar:
    # 1. Culinary Brand Identity
    st.markdown("""
    <div class="sidebar-brand-box">
        <span class="sidebar-brand-icon">🍲</span>
        <div>
            <div class="sidebar-brand-title">Food Waste System</div>
            <div class="sidebar-brand-sub">Dining & Kitchen Management</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Live Kitchen Telemetry Card
    rec_count = get_record_count()
    st.markdown(f"""
    <div class="telemetry-card">
        <div class="telemetry-pill">
            <span class="pulse-dot"></span>
            <span>SYSTEM ONLINE</span>
        </div>
        <div class="telemetry-num">{rec_count} Records Synced</div>
    </div>
    """, unsafe_allow_html=True)

    # 3. Financial Benchmark Setting
    st.markdown('<div class="section-header-styled">💰 Financial Benchmark</div>', unsafe_allow_html=True)
    cost_per_kg = st.slider(
        "Cost per Kg (₹):",
        min_value=30,
        max_value=150,
        value=65,
        step=5,
        key="sidebar_cost_slider",
        help="Used to compute financial loss and What-If scenario savings."
    )

    st.markdown("---")

    # 4. Monitored Kitchen Facilities (Clean list without badges)
    st.markdown('<div class="section-header-styled">🏢 Monitored Dining Facilities</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="facility-list-wrap">
        <div class="facility-item">
            <div class="fac-left">
                <span style="font-size:1.15rem;">🏨</span>
                <div>
                    <div class="fac-name">Hostel Mess</div>
                    <div class="fac-desc">Central Bulk Dining</div>
                </div>
            </div>
        </div>
        <div class="facility-item">
            <div class="fac-left">
                <span style="font-size:1.15rem;">☕</span>
                <div>
                    <div class="fac-name">Campus Canteen</div>
                    <div class="fac-desc">Daily Fast Casual</div>
                </div>
            </div>
        </div>
        <div class="facility-item">
            <div class="fac-left">
                <span style="font-size:1.15rem;">🍽️</span>
                <div>
                    <div class="fac-name">Executive Dining</div>
                    <div class="fac-desc">Multi-Course Service</div>
                </div>
            </div>
        </div>
        <div class="facility-item">
            <div class="fac-left">
                <span style="font-size:1.15rem;">🍱</span>
                <div>
                    <div class="fac-name">Catering Services</div>
                    <div class="fac-desc">Buffets & Special Events</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # 5. Database Reset / Sync Action
    if st.button("🔄 Reload Baseline Database", use_container_width=True, key="sidebar_reset_btn"):
        if os.path.exists(DEFAULT_CSV_PATH):
            raw_sample = pd.read_csv(DEFAULT_CSV_PATH)
            execute_backend_pipeline(raw_sample, "Verified Baseline Dataset (420 records)")
            st.success("Baseline database synchronized!")
            st.rerun()

# ----------------- MAIN BRAND HEADER BANNER ----------------- #
st.markdown(f"""
<div class="app-brand-banner">
    <div>
        <div class="app-brand-badge">
            <span>🌿</span>
            <span>SUSTAINABLE DINING PLATFORM • FOOD WASTE MANAGEMENT</span>
        </div>
        <div class="app-brand-title">
            <span>🍲</span> Food Waste <span style="color:{c_accent_saffron};">Analytics</span> & Operations
        </div>
        <div class="app-brand-subtitle">
            Smart Dining Intelligence • Continuous Kitchen Telemetry, Plate Waste Audits & Cost Optimization
        </div>
    </div>
    <div class="header-badges-wrap">
        <div class="kitchen-status-pill">
            <span class="pulse-dot"></span>
            <span>Live Telemetry Active</span>
        </div>
        <div class="header-info-chip">
            <span>🏢 4 Monitored Facilities</span>
        </div>
        <div class="header-info-chip">
            <span>🍽️ 3 Daily Meal Sessions</span>
        </div>
        <div class="header-info-chip">
            <span>📋 {rec_count} Verified Batches</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ----------------- TOP FAST-FILTER BAR ----------------- #
active_data = st.session_state.active_df

if active_data is not None and not active_data.empty and 'Date' in active_data.columns:
    min_d = pd.to_datetime(active_data['Date']).min().date()
    max_d = pd.to_datetime(active_data['Date']).max().date()

    with st.container(border=True):
        f_col_l, f_col_r = st.columns([2.5, 1])
        with f_col_l:
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:0.5rem; margin-bottom:0.25rem;">
                <span style="font-size:1.05rem;">🔍</span>
                <span style="font-size:0.92rem; font-weight:700; color:{c_text_main};">Operational Dining Filters & Horizon</span>
                <span style="background:{c_tag_bg}; border:1px solid {c_tag_border}; color:{c_accent_saffron}; font-size:0.70rem; font-weight:700; padding:2px 8px; border-radius:12px;">Live Filter Stream</span>
            </div>
            """, unsafe_allow_html=True)
        with f_col_r:
            st.markdown(f"""
            <div style="text-align:right; font-size:0.75rem; color:{c_text_dim}; padding-top:4px;">
                Auditing <strong>{len(active_data):,} logged records</strong>
            </div>
            """, unsafe_allow_html=True)

        fc1, fc2, fc3, fc4 = st.columns([1.5, 1.2, 1.2, 1.5])

        with fc1:
            all_facilities = ['All Facilities'] + sorted(list(active_data['Location'].dropna().unique()))
            sel_facility = st.selectbox("🏢 Dining Facility:", all_facilities, index=0, key="top_facility_sel")

        with fc2:
            all_meals = ['All Meals'] + sorted(list(active_data['Meal_Type'].dropna().unique())) if 'Meal_Type' in active_data.columns else ['All Meals']
            sel_meal = st.selectbox("🍽️ Meal Session:", all_meals, index=0, key="top_meal_sel")

        with fc3:
            all_cats = ['All Categories'] + sorted(list(active_data['Food_Category'].dropna().unique()))
            sel_cat = st.selectbox("🥗 Food Category:", all_cats, index=0, key="top_cat_sel")

        with fc4:
            date_range_sel = st.date_input(
                "📅 Date Horizon:",
                value=(min_d, max_d),
                min_value=min_d,
                max_value=max_d,
                key="top_date_sel"
            )

    # Filter data in-memory
    filtered_df = active_data.copy()
    filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])

    if len(date_range_sel) == 2:
        s_d, e_d = pd.to_datetime(date_range_sel[0]), pd.to_datetime(date_range_sel[1])
        filtered_df = filtered_df[(filtered_df['Date'] >= s_d) & (filtered_df['Date'] <= e_d)]

    if sel_facility != 'All Facilities':
        filtered_df = filtered_df[filtered_df['Location'] == sel_facility]

    if sel_meal != 'All Meals':
        filtered_df = filtered_df[filtered_df['Meal_Type'] == sel_meal]

    if sel_cat != 'All Categories':
        filtered_df = filtered_df[filtered_df['Food_Category'] == sel_cat]
else:
    filtered_df = active_data

# ----------------- HIGH-IMPACT 5-CARD CULINARY KPI OVERVIEW ----------------- #
if filtered_df is not None and not filtered_df.empty:
    kpis = calculate_kpis(filtered_df, cost_per_kg=cost_per_kg)
    eff = kpis['total_served_kg'] * 100 / max(1, kpis['total_prepared_kg'])

    st.markdown(f"""
    <div class="kpi-deck">
        <div class="kpi-plate">
            <div class="kpi-accent-ribbon" style="background: linear-gradient(90deg, #EA580C, #F97316);"></div>
            <div class="kpi-top-bar">
                <span class="kpi-plate-title">🍲 Total Prepared</span>
                <span class="kpi-badge-pill" style="background:rgba(234,88,12,0.12); color:#EA580C; border:1px solid rgba(234,88,12,0.25);">Prepared</span>
            </div>
            <div class="kpi-plate-val">{kpis['total_prepared_kg']:,.1f} <span class="kpi-plate-unit">kg</span></div>
            <div class="kpi-plate-sub">Across {kpis['total_records']} logged meal batches</div>
        </div>
        <div class="kpi-plate">
            <div class="kpi-accent-ribbon" style="background: linear-gradient(90deg, #16A34A, #22C55E);"></div>
            <div class="kpi-top-bar">
                <span class="kpi-plate-title">🍽️ Total Served</span>
                <span class="kpi-badge-pill" style="background:rgba(22,163,74,0.12); color:#16A34A; border:1px solid rgba(22,163,74,0.25);">{eff:.1f}% Consumed</span>
            </div>
            <div class="kpi-plate-val">{kpis['total_served_kg']:,.1f} <span class="kpi-plate-unit">kg</span></div>
            <div class="kpi-plate-sub">Diner consumption efficiency</div>
        </div>
        <div class="kpi-plate">
            <div class="kpi-accent-ribbon" style="background: linear-gradient(90deg, #DC2626, #EF4444);"></div>
            <div class="kpi-top-bar">
                <span class="kpi-plate-title">🗑️ Total Wasted</span>
                <span class="kpi-badge-pill" style="background:rgba(220,38,38,0.12); color:#DC2626; border:1px solid rgba(220,38,38,0.25);">Discarded</span>
            </div>
            <div class="kpi-plate-val">{kpis['total_wasted_kg']:,.1f} <span class="kpi-plate-unit">kg</span></div>
            <div class="kpi-plate-sub">Avg {kpis['avg_waste_per_meal']:.1f} kg per session</div>
        </div>
        <div class="kpi-plate">
            <div class="kpi-accent-ribbon" style="background: linear-gradient(90deg, #D97706, #F59E0B);"></div>
            <div class="kpi-top-bar">
                <span class="kpi-plate-title">📉 Waste Rate</span>
                <span class="kpi-badge-pill" style="background:rgba(217,119,6,0.12); color:#D97706; border:1px solid rgba(217,119,6,0.25);">Target &lt; 10%</span>
            </div>
            <div class="kpi-plate-val">{kpis['overall_waste_pct']:.1f}%</div>
            <div class="kpi-plate-sub">Variance: {kpis['overall_waste_pct'] - 10.0:+.1f}% vs goal</div>
        </div>
        <div class="kpi-plate">
            <div class="kpi-accent-ribbon" style="background: linear-gradient(90deg, #B45309, #EA580C);"></div>
            <div class="kpi-top-bar">
                <span class="kpi-plate-title">💰 Financial Loss</span>
                <span class="kpi-badge-pill" style="background:rgba(180,83,9,0.12); color:#B45309; border:1px solid rgba(180,83,9,0.25);">₹{cost_per_kg}/kg</span>
            </div>
            <div class="kpi-plate-val">₹{kpis['estimated_cost_loss']:,.0f}</div>
            <div class="kpi-plate-sub">~{kpis['meals_lost']:,} meals | {kpis['carbon_footprint_kg']:,.0f} kg CO₂e</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    def nav_to_rec():
        st.session_state.seg_workflow_nav = "💡 Action Recommendations"

    def nav_to_hub():
        st.session_state.seg_workflow_nav = "🥘 Kitchen Executive Hub"

    # ----------------- ACTION RECOMMENDATIONS LAUNCHER (CLEAN, NO CLUTTER) ----------------- #
    rec_protocols = generate_waste_reduction_insights(filtered_df)

    with st.container(border=True):
        col_cta_text, col_cta_btn = st.columns([3.3, 1.4])
        with col_cta_text:
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:0.9rem; padding:4px 0;">
                <div style="width:44px; height:44px; border-radius:12px; background:linear-gradient(135deg, {c_accent_saffron} 0%, {c_accent_amber} 100%); display:flex; align-items:center; justify-content:center; font-size:1.4rem; color:#fff; box-shadow:0 3px 12px rgba(234,88,12,0.3); flex-shrink:0;">
                    💡
                </div>
                <div>
                    <div style="display:flex; align-items:center; gap:0.5rem; flex-wrap:wrap;">
                        <span style="font-size:1.02rem; font-weight:800; color:{c_text_main};">
                            Kitchen Action Recommendations
                        </span>
                        <span style="background:{c_tag_bg}; border:1px solid {c_tag_border}; color:{c_accent_saffron}; font-size:0.72rem; font-weight:700; padding:2px 8px; border-radius:12px;">
                            {len(rec_protocols)} Protocols Ready
                        </span>
                    </div>
                    <div style="font-size:0.82rem; color:{c_text_muted}; margin-top:3px;">
                        Data-backed operational interventions for batch sizing, menu portioning, and dynamic waste reduction.
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_cta_btn:
            st.markdown('<div style="padding-top:4px;">', unsafe_allow_html=True)
            st.button(
                "🚀 View Action Recommendations →",
                key="btn_open_rec_tab",
                type="primary",
                use_container_width=True,
                on_click=nav_to_rec
            )
            st.markdown('</div>', unsafe_allow_html=True)

# ----------------- DISTRIBUTED WORKFLOW NAVIGATION ----------------- #
nav_tabs = [
    "🥘 Kitchen Executive Hub",
    "🥗 Ingredient & Recipe Analytics",
    "📈 Kitchen Dynamics & Forecasting",
    "⚡ Menu Portion Simulator",
    "💡 Action Recommendations",
    "📋 Kitchen Waste Logs & Terminal"
]

if "seg_workflow_nav" not in st.session_state or st.session_state.seg_workflow_nav not in nav_tabs:
    st.session_state.seg_workflow_nav = nav_tabs[0]

selected_tab = st.segmented_control(
    "Workflow Navigation",
    options=nav_tabs,
    key="seg_workflow_nav",
    label_visibility="collapsed"
)
if not selected_tab:
    selected_tab = st.session_state.seg_workflow_nav

# ==================== TAB 1: KITCHEN EXECUTIVE HUB ==================== #
if selected_tab == "🥘 Kitchen Executive Hub":
    if filtered_df is None or filtered_df.empty:
        st.warning("No records match the current filter selection.")
    else:
        col_main_left, col_main_right = st.columns([3, 2])

        with col_main_left:
            with st.container(border=True):
                st.markdown('<div class="chart-panel-title">📈 Weekly Waste Trajectory across Categories</div>', unsafe_allow_html=True)
                fig_trend = plot_line_trend_by_group(filtered_df, group_col='Food_Category', date_freq='W', theme_mode=theme_mode)
                st.plotly_chart(fig_trend, use_container_width=True, key="dash_trend_chart")

        with col_main_right:
            with st.container(border=True):
                st.markdown('<div class="chart-panel-title">🥧 Proportional Waste by Category</div>', unsafe_allow_html=True)
                fig_donut = plot_pie_and_donut_chart(filtered_df, group_col='Food_Category', is_donut=True, theme_mode=theme_mode)
                st.plotly_chart(fig_donut, use_container_width=True, key="dash_donut_chart")

        col_b1, col_b2 = st.columns(2)

        with col_b1:
            with st.container(border=True):
                st.markdown('<div class="chart-panel-title">🏢 Waste Volume by Dining Facility</div>', unsafe_allow_html=True)
                fig_facility = plot_barchart_aggregate(filtered_df, group_col='Location', metric='sum', theme_mode=theme_mode)
                st.plotly_chart(fig_facility, use_container_width=True, key="dash_facility_bar")

        with col_b2:
            with st.container(border=True):
                st.markdown('<div class="chart-panel-title">⚠️ Root Causes of Food Loss</div>', unsafe_allow_html=True)
                fig_causes = plot_barchart_aggregate(filtered_df, group_col='Waste_Cause', metric='sum', theme_mode=theme_mode)
                st.plotly_chart(fig_causes, use_container_width=True, key="dash_causes_bar")

        # Facility Performance Summary Table
        with st.container(border=True):
            st.markdown('<div class="chart-panel-title">🏢 Facility Operations Performance Matrix</div>', unsafe_allow_html=True)
            if 'Location' in filtered_df.columns:
                loc_summary = filtered_df.groupby('Location').agg(
                    Total_Prepared_Kg=('Food_Prepared_Kg', 'sum'),
                    Total_Served_Kg=('Food_Served_Kg', 'sum'),
                    Total_Wasted_Kg=('Food_Wasted_Kg', 'sum'),
                    Meal_Count=('Food_Prepared_Kg', 'count')
                ).reset_index()
                loc_summary['Waste_Percentage'] = ((loc_summary['Total_Wasted_Kg'] / loc_summary['Total_Prepared_Kg']) * 100).round(1)
                loc_summary['Est_Cost_Loss_INR'] = (loc_summary['Total_Wasted_Kg'] * cost_per_kg).round(0).astype(int)
                loc_summary = loc_summary.sort_values(by='Total_Wasted_Kg', ascending=False)
                st.dataframe(loc_summary, use_container_width=True)

# ==================== TAB 2: INGREDIENT & RECIPE ANALYTICS ==================== #
elif selected_tab == "🥗 Ingredient & Recipe Analytics":
    st.markdown('<div class="chart-panel-title">🥗 Ingredient & Recipe Waste Analytics</div>', unsafe_allow_html=True)
    st.caption("Statistical distribution modeling, outlier diagnostics, variable correlations, and comparative category benchmarks.")

    if filtered_df is not None and not filtered_df.empty:
        sub_tab1, sub_tab2, sub_tab3, sub_tab4 = st.tabs([
            "📊 Waste Distribution Curves",
            "📦 Outlier & Anomaly Profiler",
            "📊 Category & Facility Benchmarks",
            "🔗 Metric Correlation & Regression"
        ])

        with sub_tab1:
            h_c1, h_c2 = st.columns(2)
            with h_c1:
                bins = st.slider("Select Bin Granularity:", min_value=5, max_value=50, value=20, step=5, key="hist_bins_slider")
            with h_c2:
                split_col = st.selectbox("Stratify Distribution By:", ["None", "Food_Category", "Location", "Meal_Type"], index=0, key="hist_split_sel")

            fig_hist = plot_histogram(filtered_df, column='Food_Wasted_Kg', bins=bins, color_group=split_col, theme_mode=theme_mode)
            st.plotly_chart(fig_hist, use_container_width=True, key="analytics_hist_chart")

        with sub_tab2:
            st.markdown("##### Outlier Identification via Interquartile Range (IQR)")
            box_dim = st.selectbox("Group By Attribute:", ["Food_Category", "Location", "Meal_Type", "Waste_Cause"], index=0, key="box_dim_sel")
            fig_box = plot_boxplot(filtered_df, y_col='Food_Wasted_Kg', x_col=box_dim, theme_mode=theme_mode)
            st.plotly_chart(fig_box, use_container_width=True, key="analytics_box_chart")

        with sub_tab3:
            bar_c1, bar_c2 = st.columns(2)
            with bar_c1:
                b_dim = st.selectbox("Category Dimension:", ["Food_Category", "Location", "Meal_Type", "Waste_Cause"], index=0, key="b_dim")
            with bar_c2:
                b_stat = st.radio("Aggregation Metric:", [("sum", "Total Waste (kg)"), ("mean", "Average Waste per Meal (kg)")], format_func=lambda x: x[1], key="b_stat_radio")[0]

            fig_bar = plot_barchart_aggregate(filtered_df, group_col=b_dim, metric=b_stat, theme_mode=theme_mode)
            st.plotly_chart(fig_bar, use_container_width=True, key="analytics_bar_chart")

        with sub_tab4:
            st.markdown("##### Kitchen Metrics Correlation & Scatter Analysis")
            sc1, sc2, sc3 = st.columns(3)
            with sc1:
                x_param = st.selectbox("Independent Metric (X):", ['Food_Prepared_Kg', 'Food_Served_Kg'], index=0, key="x_param_sel")
            with sc2:
                y_param = st.selectbox("Dependent Metric (Y):", ['Food_Wasted_Kg', 'Food_Served_Kg'], index=0, key="y_param_sel")
            with sc3:
                color_param = st.selectbox("Stratify Color By:", ["Food_Category", "Location", "Meal_Type", "None"], index=0, key="color_param_sel")

            scatter_fig, r_corr = plot_scatter_correlation(
                filtered_df,
                x_col=x_param,
                y_col=y_param,
                color_col=color_param if color_param != 'None' else None,
                show_trendline=True,
                theme_mode=theme_mode
            )
            st.plotly_chart(scatter_fig, use_container_width=True, key="forecast_scatter_chart")

            st.markdown(f"**Pearson Correlation ($r$):** `{r_corr:.3f}` | Linear Strength: **{'Strong' if abs(r_corr) > 0.6 else 'Moderate' if abs(r_corr) > 0.3 else 'Weak'} Positive Correlation**")

            st.markdown("##### Kitchen Metrics Correlation Heatmap")
            col_hm_l, _ = st.columns([1, 1])
            with col_hm_l:
                fig_hm = plot_correlation_heatmap_seaborn(filtered_df, theme_mode=theme_mode)
                st.pyplot(fig_hm)

# ==================== TAB 3: KITCHEN DYNAMICS & FORECASTING ==================== #
elif selected_tab == "📈 Kitchen Dynamics & Forecasting":
    st.markdown('<div class="chart-panel-title">📈 Time Series Dynamics, Smoothing & ARIMA Forecasting</div>', unsafe_allow_html=True)
    st.caption("Econometric time series models: Moving Averages, Exponential Smoothing, Seasonal Decomposition, and ARIMA(p,d,q).")

    if filtered_df is not None and not filtered_df.empty:
        ts_freq_choice = st.selectbox("Time Series Resampling Interval:", [("D", "Daily"), ("W", "Weekly")], format_func=lambda x: x[1], key="ts_choice")
        ts_data, ts_error = prepare_time_series(filtered_df, freq=ts_freq_choice[0])

        t_sub1, t_sub2, t_sub3, t_sub4 = st.tabs([
            "A. Moving Average Smoothing",
            "B. Exponential Smoothing",
            "C. Seasonal Decomposition",
            "D. ARIMA Predictive Forecast"
        ])

        with t_sub1:
            if ts_error:
                st.error(ts_error)
            else:
                k_win = st.slider("Moving Average Window Size ($k$ periods):", min_value=3, max_value=30, value=7, step=1, key="k_win_slider")
                fig_ma, _ = plot_trend_and_moving_average(ts_data, window_size=k_win, freq_label=ts_freq_choice[1], theme_mode=theme_mode)
                st.plotly_chart(fig_ma, use_container_width=True, key="forecast_ma_chart")

        with t_sub2:
            if ts_error:
                st.error(ts_error)
            else:
                alpha_factor = st.slider("Smoothing Parameter (α):", min_value=0.05, max_value=0.95, value=0.30, step=0.05, key="alpha_factor_slider")
                fig_exp, _, exp_fail = compute_exponential_smoothing(ts_data, alpha=alpha_factor, theme_mode=theme_mode)
                if exp_fail:
                    st.error(exp_fail)
                else:
                    st.plotly_chart(fig_exp, use_container_width=True, key="forecast_exp_chart")

        with t_sub3:
            if ts_error:
                st.error(ts_error)
            else:
                dc_col1, dc_col2 = st.columns(2)
                with dc_col1:
                    p_num = st.number_input("Seasonal Cycle Period (e.g. 7 for weekly meal cycle):", min_value=2, max_value=30, value=7, key="p_num_input")
                with dc_col2:
                    m_form = st.selectbox("Decomposition Form:", ["additive", "multiplicative"], key="m_form_sel")

                fig_decomp, _, d_fail = compute_seasonal_decomposition(ts_data, period=int(p_num), model=m_form, theme_mode=theme_mode)
                if d_fail:
                    st.warning(d_fail)
                else:
                    st.plotly_chart(fig_decomp, use_container_width=True, key="forecast_decomp_chart")

        with t_sub4:
            if ts_error:
                st.error(ts_error)
            else:
                ar_c1, ar_c2, ar_c3, ar_c4 = st.columns(4)
                with ar_c1:
                    ar_p = st.number_input("p (Autoregressive Order):", min_value=0, max_value=4, value=1, key="ar_p_input")
                with ar_c2:
                    ar_d = st.number_input("d (Differencing Degree):", min_value=0, max_value=2, value=1, key="ar_d_input")
                with ar_c3:
                    ar_q = st.number_input("q (Moving Average Error):", min_value=0, max_value=4, value=1, key="ar_q_input")
                with ar_c4:
                    ar_h = st.slider("Forecast Horizon (Steps):", min_value=5, max_value=30, value=14, key="ar_h_slider")

                fig_ar, forecast_tbl, ar_err = run_arima_forecast(
                    ts_data,
                    order=(int(ar_p), int(ar_d), int(ar_q)),
                    forecast_steps=ar_h,
                    theme_mode=theme_mode
                )

                if ar_err:
                    st.error(ar_err)
                else:
                    st.plotly_chart(fig_ar, use_container_width=True, key="forecast_arima_chart")
                    st.markdown("##### 📋 Projected Waste Forecast Data")
                    st.dataframe(forecast_tbl, use_container_width=True)

# ==================== TAB 4: MENU PORTION & WHAT-IF SIMULATOR ==================== #
elif selected_tab == "⚡ Menu Portion Simulator":
    st.markdown('<div class="chart-panel-title">⚡ Kitchen What-If Simulation & Waste Reduction Strategies</div>', unsafe_allow_html=True)
    st.caption("Simulate real-world interventions, model linear regression, and inspect actionable kitchen reduction protocols.")

    if filtered_df is not None and not filtered_df.empty:
        st.markdown("##### 1. Interactive 'What-If' Scenario Planning Simulator")
        sim_c1, sim_c2 = st.columns(2)
        with sim_c1:
            prep_target = st.slider("Target: Reduce Over-Preparation Waste by (%):", min_value=0, max_value=50, value=15, step=5, key="prep_target_slider")
        with sim_c2:
            plate_target = st.slider("Target: Reduce Diner Plate Waste by (%):", min_value=0, max_value=50, value=20, step=5, key="plate_target_slider")

        sim_results = simulate_waste_reduction(filtered_df, prep_reduction_pct=prep_target, plate_reduction_pct=plate_target, cost_per_kg=cost_per_kg)

        if sim_results:
            sr1, sr2, sr3, sr4 = st.columns(4)
            sr1.metric("Projected Food Rescued", f"{sim_results['total_saved_kg']:,.1f} kg")
            sr2.metric("Projected Cost Saved", f"₹{sim_results['cost_saved']:,.0f}")
            sr3.metric("Meals Rescued", f"{sim_results['meals_rescued']:,} meals")
            sr4.metric("New Projected Waste Rate", f"{sim_results['new_waste_pct']:.1f}%", delta=f"-{sim_results['pct_improvement']:.1f}%")

            st.success(f"🎯 **Simulation Outcome:** Applying a {prep_target}% over-preparation cut and {plate_target}% plate-waste reduction would rescue **{sim_results['total_saved_kg']:.1f} kg of food**, prevent **{sim_results['co2_prevented_kg']:.1f} kg of CO₂ emissions**, and lower overall waste percentage from **{sim_results['current_waste_pct']}% to {sim_results['new_waste_pct']}%**.")

        st.markdown("---")
        st.markdown("##### 2. Scikit-Learn Simple Linear Regression Model")
        reg_info = run_regression_analysis(filtered_df)
        if reg_info:
            r1, r2, r3, r4 = st.columns(4)
            r1.metric("Slope (β₁)", f"{reg_info['slope']}")
            r2.metric("Intercept (β₀)", f"{reg_info['intercept']}")
            r3.metric("R² Score", f"{reg_info['r2_score']}")
            r4.metric("RMSE", f"{reg_info['rmse']} kg")

            st.info(f"**Regression Formula:** `{reg_info['equation']}`\n\n**Interpretation:** {reg_info['explanation']}")

            fig_reg_scatter, _ = plot_scatter_correlation(filtered_df, x_col='Food_Prepared_Kg', y_col='Food_Wasted_Kg', show_trendline=True, theme_mode=theme_mode)
            st.plotly_chart(fig_reg_scatter, use_container_width=True, key="ai_reg_scatter_chart")

        st.markdown("---")
        st.info("💡 **Looking for Action Recommendations?** Switch to the dedicated **'💡 Action Recommendations'** tab above to inspect all 6 prioritized operational protocols with custom priority tier filtering, empirical findings, and follow-up verification steps.")

# ==================== TAB 5: ACTION RECOMMENDATIONS ==================== #
elif selected_tab == "💡 Action Recommendations":
    if filtered_df is None or filtered_df.empty:
        st.warning("No records match the current filter selection.")
    else:
        col_rec_top_btn, _ = st.columns([1.5, 3.5])
        with col_rec_top_btn:
            st.button("← Back to Kitchen Dashboard", key="btn_back_to_hub_top", on_click=nav_to_hub)

        # Warm Spiced Hero Banner matching culinary bistro theme (NO GREEN)
        st.markdown(f"""
        <div class="rec-hero-banner">
            <div class="rec-hero-tag">DECISION SUPPORT & GOVERNANCE</div>
            <div class="rec-hero-title">Data-Backed Kitchen Recommendations</div>
            <div class="rec-hero-sub">
                Prioritized, actionable operational interventions dynamically generated from active statistical findings to assist mess supervisors, canteen managers, and procurement officers.
            </div>
            <div class="rec-hero-pills">
                <span class="rec-hero-pill">✦ Dynamic Generation</span>
                <span class="rec-hero-pill">✦ Prioritized Actions</span>
                <span class="rec-hero-pill">✦ Post-Action Monitoring</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        rec_tier = st.selectbox(
            "Filter Recommendations by Priority Tier:",
            ["All Priorities", "High Priority", "Medium Priority", "Low Priority"],
            key="rec_priority_filter_select"
        )

        all_rec = generate_waste_reduction_insights(filtered_df)
        if rec_tier == "High Priority":
            filtered_rec = [p for p in all_rec if p['priority'] == 'HIGH']
        elif rec_tier == "Medium Priority":
            filtered_rec = [p for p in all_rec if p['priority'] == 'MEDIUM']
        elif rec_tier == "Low Priority":
            filtered_rec = [p for p in all_rec if p['priority'] == 'LOW']
        else:
            filtered_rec = all_rec

        st.markdown(f"#### 📋 Prioritized Kitchen Protocols ({len(filtered_rec)} Active)")

        for p in filtered_rec:
            p_color = "#DC2626" if p['priority'] == 'HIGH' else "#EA580C" if p['priority'] == 'MEDIUM' else "#D97706"
            badge_class = f"priority-badge-{p['priority'].lower()}"
            st.markdown(f"""
            <div class="protocol-card" style="border-left: 5px solid {p_color};">
                <div class="protocol-header">
                    <div class="protocol-title-wrap">
                        <span style="font-size:1.25rem;">{p.get('icon', '🍲')}</span>
                        <span class="protocol-title">{p['title']}</span>
                    </div>
                    <span class="{badge_class}">Priority: {p['priority']}</span>
                </div>
                <div class="protocol-focus">Operational Focus: {p['focus']}</div>
                <div class="protocol-finding"><strong>Empirical Finding:</strong> {p['finding']}</div>
                <div class="protocol-action-box">
                    <div class="protocol-action-label">RECOMMENDED ACTION</div>
                    <div class="protocol-action-text">{p['action']}</div>
                </div>
                <div class="protocol-followup">
                    <span>🔍</span>
                    <span><strong>Verification & Follow-up:</strong> {p['followup']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ==================== TAB 6: KITCHEN LOGS & RECORD TERMINAL ==================== #
elif selected_tab == "📋 Kitchen Waste Logs & Terminal":
    st.markdown('<div class="chart-panel-title">📋 Kitchen Observation Logs & Record Search</div>', unsafe_allow_html=True)
    st.caption("Search, filter, export, and record new daily kitchen waste observations.")

    if active_data is not None and not active_data.empty:
        search_col, export_col = st.columns([3, 1])
        with search_col:
            search_query = st.text_input("🔍 Live keyword search:", placeholder="Search by category, facility, cause, or date (e.g. Rice, Spoilage, Hostel, 2026-02)...", key="log_search_input")
        with export_col:
            st.write("")
            csv_bytes = convert_df_to_csv(filtered_df)
            st.download_button(
                label="📥 Export Filtered Logs (CSV)",
                data=csv_bytes,
                file_name="food_waste_filtered_logs.csv",
                mime="text/csv",
                use_container_width=True,
                key="download_filtered_logs_btn"
            )

        log_display = filtered_df.sort_values(by='Date', ascending=False).copy()
        if search_query:
            q = search_query.lower()
            mask = (
                log_display['Food_Category'].astype(str).str.lower().str.contains(q) |
                log_display['Location'].astype(str).str.lower().str.contains(q) |
                log_display['Meal_Type'].astype(str).str.lower().str.contains(q) |
                log_display['Waste_Cause'].astype(str).str.lower().str.contains(q) |
                log_display['Date'].astype(str).str.contains(q)
            )
            log_display = log_display[mask]

        st.caption(f"Showing **{len(log_display)}** observations matching criteria:")
        display_preview = log_display.copy()
        display_preview['Date'] = display_preview['Date'].dt.strftime('%Y-%m-%d')
        st.dataframe(display_preview, use_container_width=True)

        st.markdown("---")
        # Functional Kitchen Logging Form
        with st.expander("➕ Log New Kitchen Entry (Append to SQLite Database)"):
            st.markdown("Record a new operational meal waste measurement:")
            with st.form("new_entry_form", clear_on_submit=True):
                c_form1, c_form2, c_form3 = st.columns(3)
                with c_form1:
                    entry_date = st.date_input("Entry Date:", value=datetime.today().date(), key="new_entry_date")
                    entry_location = st.selectbox("Facility:", ['Hostel', 'Canteen', 'Restaurant', 'Catering'], key="new_entry_loc")
                with c_form2:
                    entry_category = st.selectbox("Food Category:", ['Rice', 'Vegetables', 'Bread', 'Dairy', 'Fruits', 'Meat', 'Other'], key="new_entry_cat")
                    entry_meal = st.selectbox("Meal Session:", ['Breakfast', 'Lunch', 'Dinner'], key="new_entry_meal")
                with c_form3:
                    entry_cause = st.selectbox("Waste Cause:", ['Plate Waste', 'Over-preparation', 'Spoilage', 'Kitchen Trimmings', 'Expired Ingredients', 'Poor Storage'], key="new_entry_cause")

                c_quant1, c_quant2, c_quant3 = st.columns(3)
                with c_quant1:
                    entry_prep = st.number_input("Food Prepared (kg):", min_value=1.0, max_value=500.0, value=50.0, step=1.0)
                with c_quant2:
                    entry_serv = st.number_input("Food Served (kg):", min_value=0.0, max_value=500.0, value=45.0, step=1.0)
                with c_quant3:
                    entry_waste = st.number_input("Food Wasted (kg):", min_value=0.0, max_value=500.0, value=5.0, step=0.5)

                submitted = st.form_submit_button("💾 Save Record to Database", type="primary")
                if submitted:
                    if entry_serv > entry_prep:
                        st.error("Validation Error: Food Served cannot exceed Food Prepared.")
                    elif entry_waste > entry_serv:
                        st.error("Validation Error: Food Wasted cannot exceed Food Served.")
                    else:
                        new_record = {
                            'Date': str(entry_date),
                            'Food_Category': entry_category,
                            'Location': entry_location,
                            'Meal_Type': entry_meal,
                            'Food_Prepared_Kg': round(entry_prep, 1),
                            'Food_Served_Kg': round(entry_serv, 1),
                            'Food_Wasted_Kg': round(entry_waste, 1),
                            'Waste_Cause': entry_cause
                        }
                        insert_kitchen_log_entry(new_record)
                        # Reload active dataset
                        updated_all = active_data.copy()
                        new_row_df = pd.DataFrame([new_record])
                        new_row_df['Date'] = pd.to_datetime(new_row_df['Date'])
                        new_row_df['Waste_Percentage'] = ((new_row_df['Food_Wasted_Kg'] / new_row_df['Food_Prepared_Kg']) * 100).round(2)
                        st.session_state.active_df = pd.concat([updated_all, new_row_df], ignore_index=True)
                        st.success(f"Record successfully logged and synced with SQLite! Total records: {get_record_count()}")
                        st.rerun()

# ----------------- FOOTER ----------------- #
st.markdown("---")
st.markdown("""
<div style="display:flex; justify-content:space-between; align-items:center; color:#9C8573; font-size:0.8rem; padding-bottom:1.5rem;">
    <span>🍲 Food Waste Analytics & Management System</span>
    <span>Enterprise Kitchen Sustainability & Resource Optimization Platform</span>
</div>
""", unsafe_allow_html=True)
