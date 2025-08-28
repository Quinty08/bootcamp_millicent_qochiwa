# Homework 13 — Productization (Final)

## Overview
This repository demonstrates the productization of a simple linear model.  
It includes:
- Clean modular code in `src/`
- Persisted model in `model/`
- Minimal Flask API in `app.py`  
- Notebook showing analysis and API testing (`notebooks/final_productization.ipynb`)
- Stakeholder-ready report (`reports/final_summary.pdf`)

**Goal:** Prepare a reproducible and handoff-ready analysis for stakeholders or other students.

---

## Project Structure

homework13/
│
├─ data/ # Raw or/and processed data
├─ notebooks/ # Final analysis notebook
│ └─ final_productization.ipynb
├─ src/ # Reusable functions
│ └─ utils.py
├─ model/ # Pickled model
│ └─ model.pkl
├─ reports/ # Stakeholder summary and test evidence
│ ├─ final_summary.pdf
│ └─ api_test_screenshot.png
├─ app.py # Flask API
├─ requirements.txt # Python dependencies
└─ README.md

## How to Run Locally

### 1. Create a virtual environment
```bash
python -m venv .venv
# Activate the environment:
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

### 2. pip install -r requirements.txt
### 3. python app.py
The API will run locally at http://127.0.0.1:5000.

### 4. Test API
import requests
resp = requests.post('http://127.0.0.1:5000/predict', json={'features':[2.5]})
print(resp.json())

**Model Persistence**

The trained linear model is stored as model/model.pkl.
Load it in Python:

from src.utils import load_model, predict_model

model = load_model('model/model.pkl')
prediction = predict_model(model, [2.5])
print(prediction)


Assumptions & Risks

Synthetic data is used for demonstration.

Model expects 1 input feature; additional features will cause errors.

Flask API is for demonstration; not for production use.

Missing or malformed input to /predict will return an error JSON.
