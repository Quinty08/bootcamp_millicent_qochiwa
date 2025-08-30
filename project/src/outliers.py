# src/outliers.py
import numpy as np
import pandas as pd
from typing import List, Tuple

NUMERIC_DTYPES = ["int16","int32","int64","float16","float32","float64"]

def _numeric_cols(df: pd.DataFrame, include: List[str] | None = None,
                  exclude: List[str] | None = None) -> List[str]:
    cols = include if include else df.select_dtypes(include=NUMERIC_DTYPES).columns.tolist()
    exclude = exclude or []
    return [c for c in cols if c not in exclude]

def iqr_bounds(s: pd.Series, k: float = 1.5) -> Tuple[float, float]:
    s = pd.to_numeric(s, errors="coerce")
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = q3 - q1
    return q1 - k * iqr, q3 + k * iqr

def detect_outliers_iqr(
    df: pd.DataFrame,
    cols: List[str] | None = None,
    k: float = 1.5,
    exclude: List[str] | None = None
) -> tuple[pd.Series, pd.DataFrame]:
    """
    Returns:
      mask  -> boolean Series (True where row has an outlier in any selected column)
      table -> per-column summary with bounds and counts
    """
    cols = _numeric_cols(df, include=cols, exclude=exclude)
    overall_mask = pd.Series(False, index=df.index)
    records = []
    for c in cols:
        s = pd.to_numeric(df[c], errors="coerce")
        low, high = iqr_bounds(s, k)
        m = (s < low) | (s > high)
        overall_mask |= m.fillna(False)
        records.append({
            "column": c,
            "lower_bound": low,
            "upper_bound": high,
            "n_outliers": int(m.sum()),
            "pct_outliers": float(m.mean() * 100.0)
        })
    summary = pd.DataFrame(records).sort_values("pct_outliers", ascending=False)
    return overall_mask, summary

def winsorize_iqr(
    df: pd.DataFrame,
    cols: List[str] | None = None,
    k: float = 1.5,
    exclude: List[str] | None = None
) -> pd.DataFrame:
    """Cap values outside IQR bounds back to the bounds (a.k.a. winsorize)."""
    df2 = df.copy()
    cols = _numeric_cols(df2, include=cols, exclude=exclude)
    for c in cols:
        s = pd.to_numeric(df2[c], errors="coerce")
        low, high = iqr_bounds(s, k)
        df2[c] = s.clip(lower=low, upper=high)
    return df2

def remove_outliers_iqr(
    df: pd.DataFrame,
    cols: List[str] | None = None,
    k: float = 1.5,
    exclude: List[str] | None = None
) -> pd.DataFrame:
    """Drop rows where ANY selected column is outside its IQR bounds."""
    mask, _ = detect_outliers_iqr(df, cols=cols, k=k, exclude=exclude)
    return df.loc[~mask].copy()

def summarize_outliers(
    df: pd.DataFrame,
    cols: List[str] | None = None,
    k: float = 1.5,
    exclude: List[str] | None = None
) -> pd.DataFrame:
    """Convenience wrapper that just returns the summary table."""
    _, summary = detect_outliers_iqr(df, cols=cols, k=k, exclude=exclude)
    return summary
