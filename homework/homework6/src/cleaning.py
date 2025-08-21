# src/cleaning.py
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def fill_missing_median(df, columns):
    """
    Fill missing values in specified numeric columns with the median.
    
    Parameters:
    df (pd.DataFrame): Input DataFrame
    columns (list): List of column names to fill
    
    Returns:
    pd.DataFrame: DataFrame with missing values filled
    """
    df_copy = df.copy()
    for col in columns:
        if col in df_copy.columns:
            median_value = df_copy[col].median()
            df_copy[col].fillna(median_value, inplace=True)
    return df_copy

def drop_missing(df, threshold=0.5):
    """
    Drop rows with missing values exceeding the threshold.
    
    Parameters:
    df (pd.DataFrame): Input DataFrame
    threshold (float): Max proportion of allowed missing values (0-1)
    
    Returns:
    pd.DataFrame: DataFrame with rows dropped
    """
    df_copy = df.copy()
    df_copy = df_copy[df_copy.isnull().mean(axis=1) <= threshold]
    return df_copy

def normalize_data(df, columns):
    """
    Normalize numeric columns to 0-1 range using MinMax scaling.
    
    Parameters:
    df (pd.DataFrame): Input DataFrame
    columns (list): List of numeric columns to normalize
    
    Returns:
    pd.DataFrame: DataFrame with normalized columns
    """
    df_copy = df.copy()
    scaler = MinMaxScaler()
    df_copy[columns] = scaler.fit_transform(df_copy[columns])
    return df_copy
