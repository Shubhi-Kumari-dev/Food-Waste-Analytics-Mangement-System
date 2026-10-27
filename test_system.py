"""
Automated System Verification Script for Food Waste Analytics and Management System.
Tests data processing, database operations, visualization rendering,
time series modeling, recommendations, and regression.
"""

import sys
import os
import pandas as pd
import numpy as np

# Ensure utils can be imported
sys.path.insert(0, os.path.dirname(__file__))

from utils.data_processing import (
    load_data_file,
    validate_columns,
    get_data_quality_report,
    clean_food_waste_data,
    calculate_kpis,
    REQUIRED_COLUMNS
)
from utils.database import (
    get_database_engine,
    save_data_to_db,
    load_all_records_from_db,
    get_record_count,
    run_custom_query,
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
    generate_waste_reduction_insights
)

def run_tests():
    print("=" * 60)
    print("[TEST] RUNNING SYSTEM VERIFICATION SUITE")
    print("=" * 60)

    # Test 1: Verify Sample CSV Exists and Loads
    csv_path = os.path.join(os.path.dirname(__file__), "data", "food_waste_sample.csv")
    assert os.path.exists(csv_path), f"Sample CSV missing at {csv_path}"
    df = pd.read_csv(csv_path)
    print(f"[PASS] Test 1: Sample CSV loaded successfully with {len(df)} rows.")

    # Test 2: Column Validation
    is_valid, missing, existing = validate_columns(df)
    assert is_valid, f"Column validation failed: missing {missing}"
    print(f"[PASS] Test 2: All required columns present: {REQUIRED_COLUMNS}")

    # Test 3: Data Cleaning
    cleaned_df, log = clean_food_waste_data(df, handle_missing="mean_mode", remove_duplicates=True)
    assert not cleaned_df.empty, "Cleaned DataFrame is empty"
    assert (cleaned_df['Food_Prepared_Kg'] >= 0).all(), "Negative prepared quantities found"
    assert (cleaned_df['Food_Served_Kg'] >= 0).all(), "Negative served quantities found"
    assert (cleaned_df['Food_Wasted_Kg'] >= 0).all(), "Negative wasted quantities found"
    print(f"[PASS] Test 3: Data cleaning validated. Constraints verified.")

    # Test 4: KPI Calculation
    kpis = calculate_kpis(cleaned_df)
    assert kpis['total_records'] == len(cleaned_df)
    assert kpis['total_wasted_kg'] > 0
    assert 0 <= kpis['overall_waste_pct'] <= 100
    print(f"[PASS] Test 4: KPIs calculated. Overall Waste: {kpis['overall_waste_pct']}%.")

    # Test 5: Database Operations (to_sql & query)
    save_ok, msg = save_data_to_db(cleaned_df, mode="replace")
    assert save_ok, f"Database save failed: {msg}"
    db_count = get_record_count()
    assert db_count == len(cleaned_df), f"DB count mismatch: {db_count} vs {len(cleaned_df)}"
    
    query_df, q_err = run_custom_query(f"SELECT Food_Category, SUM(Food_Wasted_Kg) as Total FROM {TABLE_NAME} GROUP BY Food_Category")
    assert q_err is None and query_df is not None and not query_df.empty
    print(f"[PASS] Test 5: SQLite database successfully loaded and queried ({db_count} rows).")

    # Test 6: Lab 7 & 8 Visualization functions
    fig1 = plot_line_trend_by_group(cleaned_df, group_col='Food_Category', date_freq='W')
    fig2, corr_r = plot_scatter_correlation(cleaned_df, x_col='Food_Prepared_Kg', y_col='Food_Wasted_Kg')
    fig3 = plot_correlation_heatmap_seaborn(cleaned_df)
    fig4 = plot_histogram(cleaned_df, column='Food_Wasted_Kg', bins=15)
    fig5 = plot_boxplot(cleaned_df, y_col='Food_Wasted_Kg', x_col='Food_Category')
    fig6 = plot_barchart_aggregate(cleaned_df, group_col='Location')
    fig7 = plot_pie_and_donut_chart(cleaned_df, group_col='Waste_Cause', is_donut=True)
    comp_df = get_chart_tools_comparison_df()
    
    assert fig1 is not None and fig2 is not None and fig3 is not None and fig4 is not None
    assert fig5 is not None and fig6 is not None and fig7 is not None and not comp_df.empty
    print(f"[PASS] Test 6: All Lab 7 & 8 chart generation functions produced valid figures (r = {corr_r:.3f}).")

    # Test 7: Time Series Modeling
    ts_series, ts_err = prepare_time_series(cleaned_df, freq='D')
    assert ts_err is None and ts_series is not None, f"Time series preparation failed: {ts_err}"
    
    ma_fig, ma_res = plot_trend_and_moving_average(ts_series, window_size=7)
    exp_fig, exp_res, exp_err = compute_exponential_smoothing(ts_series, alpha=0.3)
    decomp_fig, decomp_res, decomp_err = compute_seasonal_decomposition(ts_series, period=7, model='additive')
    arima_fig, arima_table, arima_err = run_arima_forecast(ts_series, order=(1,1,1), forecast_steps=7)
    
    assert ma_fig is not None and not ma_res.empty
    assert exp_err is None and exp_fig is not None
    assert decomp_err is None and decomp_fig is not None
    assert arima_err is None and arima_table is not None and len(arima_table) == 7
    print(f"[PASS] Test 7: Time Series suite (Moving Avg, Exp Smoothing, Decomposition, ARIMA) verified.")

    # Test 8: Recommendations & Regression
    reg_res = run_regression_analysis(cleaned_df)
    assert reg_res is not None and 'r2_score' in reg_res
    insights = generate_waste_reduction_insights(cleaned_df)
    assert len(insights) > 0, "No insights generated"
    print(f"[PASS] Test 8: Regression (R^2 = {reg_res['r2_score']}) and {len(insights)} operational insights generated.")

    # Test 9: Robust Error Handling (Bad inputs)
    bad_df = pd.DataFrame({'Random': [1, 2, 3]})
    bad_valid, bad_missing, _ = validate_columns(bad_df)
    assert not bad_valid and len(bad_missing) > 0
    short_ts = pd.Series([10, 20], index=pd.date_range('2026-01-01', periods=2))
    _, _, d_err = compute_seasonal_decomposition(short_ts, period=7)
    assert d_err is not None  # Graceful failure
    print(f"[PASS] Test 9: Negative test cases and validation guards handled safely.")

    print("=" * 60)
    print("[SUCCESS] ALL 9 TEST SUITES PASSED FLAWLESSLY!")
    print("=" * 60)

if __name__ == '__main__':
    run_tests()
