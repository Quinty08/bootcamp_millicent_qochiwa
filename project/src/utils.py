import pandas as pd


def clean_column_names(df:pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names : lowercase, replace spaces with underscores,
    
    Parameters:
        df (pd.DataFrame) : Input dataFrame

    Returns:
       pd.DataFrame : a DataFrame with cleaned column names
    """
    df=df.copy()
    df.columns =df.columns.str.strip().str.lower().str.replace(' ','_')
    return df

def fillna_values(df : pd.DataFrame)-> pd.DataFrame:
    """
    replaces NA values in the affordability column with 0
    """
    
    df=df.copy()
    df['affordability'] = df['affordability'].fillna(0)
    return df
