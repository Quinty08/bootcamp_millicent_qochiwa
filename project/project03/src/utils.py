# src/utils.py
import pandas as pd

def get_summary_stats(df):
    """
    Return summary statistics of numeric columns.
    """
    return df.describe()

def clean_column_names(df):
    """
    Make column names lowercase and replace spaces with underscores.
    """
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    return df
