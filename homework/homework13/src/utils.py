# src/utils.py
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

def generate_synthetic_data(n=200, seed=101):
    np.random.seed(seed)
    x = np.linspace(0, 10, n) + np.random.normal(0, 0.5, n)
    y = 2.0 * x + 1.0 + np.random.normal(0, 2.0, n)  # linear + noise
    df = pd.DataFrame({'x_feature': x, 'y_target': y})
    return df

def train_linear_model(df, feature_col='x_feature', target_col='y_target'):
    X = df[[feature_col]].values
    y = df[target_col].values
    model = LinearRegression().fit(X, y)
    return model

def save_model(model, path='model/model.pkl'):
    with open(path, 'wb') as f:
        pickle.dump(model, f)

def load_model(path='model/model.pkl'):
    with open(path, 'rb') as f:
        return pickle.load(f)

def predict_model(model, X):
    Xarr = np.array(X).reshape(1, -1) if np.ndim(X) == 1 else np.array(X)
    return model.predict(Xarr)
