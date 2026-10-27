"""
Data Processing Module for Food Waste Analytics and Management System.
Handles dataset loading, validation, data cleaning, missing value strategies,
duplicate checks, and KPI calculations.
"""

import pandas as pd
import numpy as np

# Standard required schema for the project
REQUIRED_COLUMNS = [
    'Date',
    'Food_Category',
    'Location',
    'Meal_Type',
    'Food_Prepared_Kg',
    'Food_Served_Kg',
    'Food_Wasted_Kg',
    'Waste_Cause'
]

NUMERIC_COLUMNS = ['Food_Prepared_Kg', 'Food_Served_Kg', 'Food_Wasted_Kg']
CATEGORICAL_COLUMNS = ['Food_Category', 'Location', 'Meal_Type', 'Waste_Cause']

def load_data_file(uploaded_file):
    """
    Loads an uploaded file (CSV or Excel) into a pandas DataFrame.
    Returns: (DataFrame or None, error_message or None)
    """
    try:
        filename = uploaded_file.name.lower()
        if filename.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif filename.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file)
        else:
            return None, "Unsupported file format. Please upload a .csv or .xlsx file."
        return df, None
    except Exception as e:
        return None, f"Error reading file: {str(e)}"

def validate_columns(df):
    """
    Validates whether the DataFrame contains all required columns.
    Returns: (is_valid, missing_columns, existing_columns)
    """
    existing_cols = list(df.columns)
    missing_cols = [col for col in REQUIRED_COLUMNS if col not in existing_cols]
    is_valid = len(missing_cols) == 0
    return is_valid, missing_cols, existing_cols

def get_data_quality_report(df):
    """
    Generates a dictionary report of dataset statistics, data types, missing values,
    and duplicate rows.
    """
    report = {
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'missing_per_column': df.isnull().sum().to_dict(),
        'total_missing': int(df.isnull().sum().sum()),
        'duplicate_rows': int(df.duplicated().sum()),
        'dtypes': {col: str(dtype) for col, dtype in df.dtypes.items()}
    }
    return report

def clean_food_waste_data(df, handle_missing="mean_mode", remove_duplicates=True):
    """
    Cleans the food waste DataFrame according to standard lab data cleaning steps:
    1. Removes duplicates if requested.
    2. Converts Date column to datetime.
    3. Converts numeric columns to float, coercing invalid entries to NaN.
    4. Handles missing values based on user preference ('drop', 'mean_mode', or 'keep').
    5. Validates non-negative constraints and logical bounds:
       - Prepared >= 0, Served >= 0, Wasted >= 0
       - Ensures Served <= Prepared and Wasted <= Served.
    Returns: (cleaned_df, cleaning_log_list)
    """
    cleaned_df = df.copy()
    log = []

    initial_count = len(cleaned_df)
    log.append(f"Initial record count: {initial_count}")

    # Step 1: Remove duplicates
    if remove_duplicates:
        dups = int(cleaned_df.duplicated().sum())
        if dups > 0:
            cleaned_df = cleaned_df.drop_duplicates()
            log.append(f"Removed {dups} duplicate row(s).")
        else:
            log.append("No duplicate rows detected.")

    # Step 2: Date Conversion
    if 'Date' in cleaned_df.columns:
        cleaned_df['Date'] = pd.to_datetime(cleaned_df['Date'], errors='coerce')
        invalid_dates = cleaned_df['Date'].isnull().sum()
        if invalid_dates > 0:
            log.append(f"Found {invalid_dates} invalid date value(s).")

    # Step 3: Numeric Conversion
    for col in NUMERIC_COLUMNS:
        if col in cleaned_df.columns:
            cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce')

    # Step 4: Handle Missing Values
    missing_before = int(cleaned_df.isnull().sum().sum())
    log.append(f"Missing values before resolution: {missing_before}")

    if handle_missing == "drop":
        cleaned_df = cleaned_df.dropna()
        dropped = initial_count - len(cleaned_df)
        log.append(f"Dropped {dropped} row(s) containing missing or invalid values.")
    elif handle_missing == "mean_mode":
        # Impute numeric columns with median (robust against outliers) or mean
        for col in NUMERIC_COLUMNS:
            if col in cleaned_df.columns and cleaned_df[col].isnull().any():
                val = cleaned_df[col].median()
                cleaned_df[col] = cleaned_df[col].fillna(val)
                log.append(f"Imputed missing '{col}' with median value: {val:.1f}")

        # Impute categorical columns with mode
        for col in CATEGORICAL_COLUMNS:
            if col in cleaned_df.columns and cleaned_df[col].isnull().any():
                mode_val = cleaned_df[col].mode()
                val = mode_val[0] if not mode_val.empty else "Unknown"
                cleaned_df[col] = cleaned_df[col].fillna(val)
                log.append(f"Imputed missing '{col}' with mode: '{val}'")
                
        # Drop rows where Date is still NaT
        if 'Date' in cleaned_df.columns and cleaned_df['Date'].isnull().any():
            cleaned_df = cleaned_df.dropna(subset=['Date'])
            log.append("Removed rows with unparseable dates.")
    else:
        log.append("Retained missing values as per user choice.")

    # Step 5: Logical Bounds & Non-negative Validation
    if all(col in cleaned_df.columns for col in NUMERIC_COLUMNS):
        # Ensure non-negative
        negative_prep = (cleaned_df['Food_Prepared_Kg'] < 0).sum()
        negative_serv = (cleaned_df['Food_Served_Kg'] < 0).sum()
        negative_wast = (cleaned_df['Food_Wasted_Kg'] < 0).sum()
        
        if negative_prep > 0 or negative_serv > 0 or negative_wast > 0:
            cleaned_df['Food_Prepared_Kg'] = cleaned_df['Food_Prepared_Kg'].abs()
            cleaned_df['Food_Served_Kg'] = cleaned_df['Food_Served_Kg'].abs()
            cleaned_df['Food_Wasted_Kg'] = cleaned_df['Food_Wasted_Kg'].abs()
            log.append("Replaced negative quantities with absolute positive values.")

        # Ensure Served <= Prepared
        inconsistent_serv = (cleaned_df['Food_Served_Kg'] > cleaned_df['Food_Prepared_Kg']).sum()
        if inconsistent_serv > 0:
            cleaned_df['Food_Served_Kg'] = cleaned_df[['Food_Served_Kg', 'Food_Prepared_Kg']].min(axis=1)
            log.append(f"Adjusted {inconsistent_serv} rows where Served > Prepared to match Prepared.")

        # Ensure Wasted <= Served
        inconsistent_wast = (cleaned_df['Food_Wasted_Kg'] > cleaned_df['Food_Served_Kg']).sum()
        if inconsistent_wast > 0:
            cleaned_df['Food_Wasted_Kg'] = cleaned_df[['Food_Wasted_Kg', 'Food_Served_Kg']].min(axis=1)
            log.append(f"Adjusted {inconsistent_wast} rows where Wasted > Served to match Served.")

    # Calculate individual record waste percentage
    if 'Food_Prepared_Kg' in cleaned_df.columns and 'Food_Wasted_Kg' in cleaned_df.columns:
        cleaned_df['Waste_Percentage'] = np.where(
            cleaned_df['Food_Prepared_Kg'] > 0,
            (cleaned_df['Food_Wasted_Kg'] / cleaned_df['Food_Prepared_Kg']) * 100,
            0.0
        ).round(2)

    final_count = len(cleaned_df)
    log.append(f"Final clean record count: {final_count}")

    return cleaned_df, log

def calculate_kpis(df, cost_per_kg=65.0):
    """
    Computes summary Key Performance Indicators (KPIs) from the current dataset,
    including economic loss and environmental impact.
    Returns: dict of formatted metrics
    """
    if df is None or df.empty:
        return {
            'total_records': 0,
            'total_prepared_kg': 0.0,
            'total_served_kg': 0.0,
            'total_wasted_kg': 0.0,
            'overall_waste_pct': 0.0,
            'avg_waste_per_meal': 0.0,
            'estimated_cost_loss': 0,
            'carbon_footprint_kg': 0.0,
            'meals_lost': 0
        }

    total_records = len(df)
    total_prepared = float(df['Food_Prepared_Kg'].sum()) if 'Food_Prepared_Kg' in df.columns else 0.0
    total_served = float(df['Food_Served_Kg'].sum()) if 'Food_Served_Kg' in df.columns else 0.0
    total_wasted = float(df['Food_Wasted_Kg'].sum()) if 'Food_Wasted_Kg' in df.columns else 0.0

    # Avoid division by zero
    if total_prepared > 0:
        overall_waste_pct = (total_wasted / total_prepared) * 100
    else:
        overall_waste_pct = 0.0

    avg_waste = (total_wasted / total_records) if total_records > 0 else 0.0
    cost_loss = round(total_wasted * cost_per_kg, 0)
    carbon_fp = round(total_wasted * 2.5, 1)
    meals_count = int(total_wasted / 0.4) if total_wasted > 0 else 0

    return {
        'total_records': total_records,
        'total_prepared_kg': round(total_prepared, 1),
        'total_served_kg': round(total_served, 1),
        'total_wasted_kg': round(total_wasted, 1),
        'overall_waste_pct': round(overall_waste_pct, 2),
        'avg_waste_per_meal': round(avg_waste, 2),
        'estimated_cost_loss': cost_loss,
        'carbon_footprint_kg': carbon_fp,
        'meals_lost': meals_count
    }

def convert_df_to_csv(df):
    """
    Encodes a DataFrame into utf-8 CSV bytes for download in Streamlit.
    """
    return df.to_csv(index=False).encode('utf-8')
