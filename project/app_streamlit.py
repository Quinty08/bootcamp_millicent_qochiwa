# app_streamlit.py
import streamlit as st
from src.utils import run_full_analysis, predict, prepare_data
import pandas as pd

st.title("Model demo — Financial Engineering project")

st.header("Make a prediction")

# --- Input fields for all real dataset features ---
age = st.number_input("age", value=30)
basic_salary = st.number_input("basic_salary", value=50000)
disbursementamount = st.number_input("disbursementamount", value=10000)
instalment = st.number_input("instalment", value=500)
interestrate = st.number_input("interestrate", value=5.0)
affordability = st.number_input("affordability", value=0.0)
# Add any additional columns from your dataset here, with default values

# Build input dictionary
input_dict = {
    "age": age,
    "basic_salary": basic_salary,
    "disbursementamount": disbursementamount,
    "instalment": instalment,
    "interestrate": interestrate,
    "affordability": affordability,
    # include rest of your columns
}

if st.button("Predict"):
    try:
        res = predict(input_dict)
        st.write("Predictions:", res["predictions"])
        st.write(f"Number of predictions: {res['n']}")
    except Exception as e:
        st.error(f"Error during prediction: {e}")

st.header("Run full analysis")
if st.button("Run Full Analysis"):
    try:
        summary = run_full_analysis(force_retrain=True)
        st.write("Full analysis complete. See reports folder.")
        st.json(summary)
    except Exception as e:
        st.error(f"Error during full analysis: {e}")

st.header("Notes")
st.write("All predictions use the RandomForestRegressor trained on your project dataset.")
