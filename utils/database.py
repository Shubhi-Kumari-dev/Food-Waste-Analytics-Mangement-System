"""
Database Module for Food Waste Analytics and Management System (Practical 5).
Handles SQLite database connection via SQLAlchemy, table initialization,
loading DataFrames via to_sql(), running SQL queries, and filtering records.
"""

import os
import pandas as pd
from sqlalchemy import create_engine, text, inspect

# Relative or absolute database path
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database')
DB_FILE = os.path.join(DB_DIR, 'food_waste.db')
TABLE_NAME = 'food_waste_records'

def get_database_engine():
    """
    Creates and returns an SQLAlchemy engine connected to the SQLite database.
    Ensures the parent database directory exists.
    """
    os.makedirs(DB_DIR, exist_ok=True)
    connection_url = f"sqlite:///{DB_FILE}"
    engine = create_engine(connection_url, echo=False)
    return engine

def check_table_exists():
    """
    Checks if the food_waste_records table exists in the database.
    """
    engine = get_database_engine()
    inspector = inspect(engine)
    return TABLE_NAME in inspector.get_table_names()

def get_record_count():
    """
    Returns the total number of records currently stored in the database table.
    """
    if not check_table_exists():
        return 0
    engine = get_database_engine()
    try:
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {TABLE_NAME}"))
            count = result.scalar()
            return count if count is not None else 0
    except Exception:
        return 0

def save_data_to_db(df, mode="append"):
    """
    Saves a cleaned DataFrame to the SQLite database using pandas to_sql().
    Parameters:
        df: pandas DataFrame
        mode: 'append' to add new records or 'replace' to overwrite existing table.
    Returns: (success_boolean, message)
    """
    if df is None or df.empty:
        return False, "Cannot save an empty dataset to the database."

    engine = get_database_engine()
    df_to_save = df.copy()

    # Convert datetime to string format (YYYY-MM-DD) for clean SQLite storage
    if 'Date' in df_to_save.columns:
        df_to_save['Date'] = pd.to_datetime(df_to_save['Date']).dt.strftime('%Y-%m-%d')

    try:
        # Use pandas to_sql via SQLAlchemy engine
        df_to_save.to_sql(
            name=TABLE_NAME,
            con=engine,
            if_exists=mode,
            index=False
        )
        total_now = get_record_count()
        return True, f"Successfully saved {len(df_to_save)} records ({mode} mode). Total records in DB: {total_now}."
    except Exception as e:
        return False, f"Failed to save data to database: {str(e)}"

def load_all_records_from_db():
    """
    Extracts all records from the SQLite database table into a pandas DataFrame.
    """
    if not check_table_exists():
        return pd.DataFrame()
    engine = get_database_engine()
    try:
        query = f"SELECT * FROM {TABLE_NAME} ORDER BY Date ASC"
        df = pd.read_sql_query(query, engine)
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
        return df
    except Exception as e:
        print(f"Error loading records from database: {e}")
        return pd.DataFrame()

def run_custom_query(query_str):
    """
    Executes a custom SQL SELECT query on the database and returns a pandas DataFrame.
    """
    if not check_table_exists():
        return None, "Database table does not exist yet. Please load data first."
    engine = get_database_engine()
    try:
        df = pd.read_sql_query(query_str, engine)
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='ignore')
        return df, None
    except Exception as e:
        return None, f"SQL Query Error: {str(e)}"

def filter_records_sql(start_date=None, end_date=None, category=None, location=None):
    """
    Demonstrates SQL parameterization and filtering by Date, Category, and Location.
    """
    if not check_table_exists():
        return pd.DataFrame()

    engine = get_database_engine()
    query = f"SELECT * FROM {TABLE_NAME} WHERE 1=1"
    params = {}

    if start_date:
        query += " AND Date >= :start_date"
        params['start_date'] = str(start_date)
    if end_date:
        query += " AND Date <= :end_date"
        params['end_date'] = str(end_date)
    if category and category != 'All':
        query += " AND Food_Category = :category"
        params['category'] = category
    if location and location != 'All':
        query += " AND Location = :location"
        params['location'] = location

    query += " ORDER BY Date ASC"

    try:
        with engine.connect() as conn:
            df = pd.read_sql_query(text(query), conn, params=params)
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date'])
            return df
    except Exception as e:
        print(f"Filter query error: {e}")
        return pd.DataFrame()

def insert_kitchen_log_entry(record_dict):
    """
    Inserts a single kitchen waste observation log into the SQLite database table.
    """
    df_new = pd.DataFrame([record_dict])
    return save_data_to_db(df_new, mode="append")
