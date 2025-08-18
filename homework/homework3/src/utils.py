# src/utils.py


def get_summary_stats(df):
    """return summary stats of numerical columns"""
    return df.describe()