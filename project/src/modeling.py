# src/modeling.py
import os
import re
import numpy as np
import pandas as pd

from dotenv import load_dotenv

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LinearRegression, RidgeCV, LassoCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

import matplotlib.pyplot as plt
from scipy import stats

load_dotenv()

# ---------- IO ----------
def load_features(path_env_key="FEATURES_DATA_CSV",
                  default_path="data/processed/loan_data_features.csv",
                  parse_dates=("LoanDate","DisbursementDate","LastPaymentDate","RetirementDate")):
    path = os.getenv(path_env_key, default_path)
    parse = [c for c in (parse_dates or []) if isinstance(c, str)]
    df = pd.read_csv(path, parse_dates=[c for c in parse if c in pd.read_csv(path, nrows=0).columns])
    return df

# ---------- Feature typing ----------
def infer_feature_types(df, target, drop_patterns=("id", "number"), date_like=("date", "time")):
    """
    Returns numeric_cols, categorical_cols, dropped_cols according to column names and dtypes.
    - Excludes target and ID-like fields from modeling features.
    """
    cols = [c for c in df.columns if c != target]
    id_regex = re.compile("|".join(drop_patterns), re.I) if drop_patterns else None
    date_regex = re.compile("|".join(date_like), re.I) if date_like else None

    drop = []
    for c in cols:
        if id_regex and id_regex.search(c):
            drop.append(c)
        elif date_regex and date_regex.search(c):
            drop.append(c)

    use_cols = [c for c in cols if c not in drop]
    num_cols = [c for c in use_cols if pd.api.types.is_numeric_dtype(df[c])]
    cat_cols = [c for c in use_cols if c not in num_cols]

    return num_cols, cat_cols, drop

# ---------- Split ----------
def time_aware_split(df, date_col="LoanDate", test_size=0.2, random_state=42):
    if date_col in df.columns and df[date_col].notna().any():
        df2 = df.sort_values(date_col)
        n = len(df2)
        cut = int((1 - test_size) * n)
        train_df = df2.iloc[:cut].copy()
        test_df  = df2.iloc[cut:].copy()
    else:
        train_df, test_df = train_test_split(df, test_size=test_size, random_state=random_state)
    return train_df, test_df

# ---------- Pipelines ----------
def make_preprocessor(numeric_cols, categorical_cols):
    numeric_pipe = Pipeline(steps=[
        ("scaler", StandardScaler())
    ])
    cat_pipe = Pipeline(steps=[
        ("ohe", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])
    pre = ColumnTransformer(
        transformers=[
            ("num", numeric_pipe, numeric_cols),
            ("cat", cat_pipe, categorical_cols)
        ],
        remainder="drop"
    )
    return pre

def make_model_pipeline(model, numeric_cols, categorical_cols):
    pre = make_preprocessor(numeric_cols, categorical_cols)
    pipe = Pipeline(steps=[
        ("pre", pre),
        ("model", model)
    ])
    return pipe

# ---------- Train/Eval ----------
def eval_regression(y_true, y_pred):
    """
    Return MAE, RMSE, R2 for numeric regression.
    Compatible with scikit-learn versions that don't accept `squared=` keyword.
    """
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)   # returns MSE
    rmse = np.sqrt(mse)                        # compute RMSE manually
    r2 = r2_score(y_true, y_pred)
    return {"MAE": mae, "RMSE": rmse, "R2": r2}
def fit_and_report(model_name, model, X_train, y_train, X_test, y_test, num_cols, cat_cols):
    pipe = make_model_pipeline(model, num_cols, cat_cols)
    pipe.fit(X_train, y_train)
    yhat = pipe.predict(X_test)
    metrics = eval_regression(y_test, yhat)
    return model_name, pipe, metrics, yhat

def try_baselines(X_train, y_train, X_test, y_test, num_cols, cat_cols):
    candidates = {
        "Linear": LinearRegression(),
        "RidgeCV": RidgeCV(alphas=[0.1, 1.0, 10.0]),
        "LassoCV": LassoCV(alphas=[0.001, 0.01, 0.1, 1.0], max_iter=5000, random_state=42),
        "RandomForest": RandomForestRegressor(n_estimators=250, random_state=42, n_jobs=-1)
    }
    rows, fitted = [], {}
    for name, mdl in candidates.items():
        name, pipe, m, yhat = fit_and_report(name, mdl, X_train, y_train, X_test, y_test, num_cols, cat_cols)
        rows.append({"model": name, **m})
        fitted[name] = (pipe, yhat)
    metrics_df = pd.DataFrame(rows).sort_values("RMSE")
    return metrics_df, fitted

# ---------- Diagnostics ----------
def residual_plots(y_true, y_pred, title_prefix=""):
    resid = y_true - y_pred
    # Residuals vs Fitted
    plt.figure(figsize=(6,4))
    plt.scatter(y_pred, resid, alpha=0.5)
    plt.axhline(0, linestyle="--")
    plt.xlabel("Fitted values")
    plt.ylabel("Residuals")
    plt.title(f"{title_prefix} Residuals vs Fitted")
    plt.show()

    # QQ plot
    plt.figure(figsize=(6,4))
    stats.probplot(resid, dist="norm", plot=plt)
    plt.title(f"{title_prefix} Residuals QQ Plot")
    plt.show()

def linear_coeff_table(fitted_pipe):
    """
    Works for Linear/Ridge/Lasso pipelines.
    Returns DataFrame of coefficients aligned with feature names.
    """
    model = fitted_pipe.named_steps["model"]
    pre = fitted_pipe.named_steps["pre"]

    # Get feature names back from ColumnTransformer
    num_names = pre.transformers_[0][2]
    ohe = pre.transformers_[1][1].named_steps["ohe"]
    cat_original = pre.transformers_[1][2]
    cat_names = list(ohe.get_feature_names_out(cat_original))

    feat_names = list(num_names) + cat_names

    if hasattr(model, "coef_"):
        coefs = model.coef_.ravel()
        return pd.DataFrame({"feature": feat_names, "coef": coefs}).sort_values("coef", key=abs, ascending=False)
    else:
        return pd.DataFrame({"feature": feat_names})



