# src/utils.py
import os
import json
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# --- Paths ---
ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "model"
REPORTS_DIR = ROOT / "reports"
DATA_DIR = ROOT / "data" / "processed"

MODEL_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# --- Existing cleaning functions ---
def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    return df

def fillna_values(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "affordability" in df.columns:
        df['affordability'] = df['affordability'].fillna(0)
    return df

# --- Data prep ---
def prepare_data(path=None):
    """
    Loads and preprocesses the real project dataset.
    Returns X (features) and y (target).
    """
    if path is None:
        path = DATA_DIR / "cleaned_loan_data_capped.csv"

    df = pd.read_csv(path)
    df = clean_column_names(df)
    df = fillna_values(df)

    target_column = "affordability"  # your regression target
    if target_column not in df.columns:
        raise ValueError(f"Target column '{target_column}' not found in dataset")

    # drop non-numeric columns (IDs, text)
    non_numeric_cols = df.select_dtypes(include=["object"]).columns.tolist()
    X = df.drop(columns=[target_column] + non_numeric_cols)
    y = df[target_column]
    return X, y

# --- Model handling ---
def save_model(model, name="model_v1.pkl"):
    path = MODEL_DIR / name
    joblib.dump(model, path)
    return str(path)

def load_model(name="model_v1.pkl"):
    path = MODEL_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"Model not found at {path}")
    return joblib.load(path)

# --- Training ---
def train_and_save(default_model_name="model_v1.pkl", overwrite=True):
    X, y = prepare_data()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    rmse = mean_squared_error(y_test, preds) ** 0.5

    # save model
    if overwrite or not (MODEL_DIR / default_model_name).exists():
        save_model(model, default_model_name)

    # write metrics and test predictions
    REPORTS_DIR.mkdir(exist_ok=True)
    metrics_path = REPORTS_DIR / "metrics.json"
    with open(metrics_path, "w") as f:
        json.dump({"rmse": float(rmse)}, f, indent=2)

    pd.DataFrame({"y_true": y_test, "y_pred": preds}).to_csv(REPORTS_DIR / "test_predictions.csv", index=False)
    return {"model_path": str(MODEL_DIR / default_model_name), "metrics": {"rmse": float(rmse)}}

# --- Prediction ---
def predict(input_data, model_name="model_v1.pkl"):
    model = load_model(model_name)
    if isinstance(input_data, dict):
        X = pd.DataFrame([input_data])
    elif isinstance(input_data, list):
        X = pd.DataFrame(input_data)
    elif isinstance(input_data, pd.DataFrame):
        X = input_data
    else:
        raise ValueError("Input must be dict, list of dicts, or DataFrame")
    preds = model.predict(X)
    return {"predictions": preds.tolist(), "n": len(preds)}

# --- Plotting ---
def plot_example(save_path=REPORTS_DIR / "example_plot.png"):
    try:
        model = load_model()
    except FileNotFoundError:
        train_and_save()
        model = load_model()

    if hasattr(model, "feature_importances_"):
        fi = model.feature_importances_
        X, _ = prepare_data()
        names = X.columns.tolist()
        plt.figure(figsize=(10,6))
        plt.bar(names, fi)
        plt.xticks(rotation=45, ha="right")
        plt.title("Feature Importances")
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()
        return str(save_path)
    return None

# --- Full analysis orchestrator ---
def run_full_analysis(force_retrain=False):
    model_file = MODEL_DIR / "model_v1.pkl"
    if not model_file.exists() or force_retrain:
        result = train_and_save(overwrite=True)
    else:
        result = {"model_path": str(model_file)}

    plot_path = plot_example()

    try:
        preds_df = pd.read_csv(REPORTS_DIR / "test_predictions.csv")
    except FileNotFoundError:
        preds_df = pd.DataFrame()

    summary = {
        "model": result["model_path"],
        "plot": plot_path,
        "notes": "Trained and saved; see metrics.json for details"
    }
    with open(REPORTS_DIR / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    return summary
