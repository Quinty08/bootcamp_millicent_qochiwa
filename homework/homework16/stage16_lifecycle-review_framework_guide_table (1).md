# Applied Financial Engineering — Framework Guide Template

This Framework Guide is a structured reflection tool.  
Fill it in as you progress through the course or at the end of your project.  
It will help you connect each stage of the **Applied Financial Engineering Lifecycle** to your own project, and create a portfolio-ready artifact.

---

## How to Use
- Each row corresponds to one stage in the lifecycle.  
- Use the prompts to guide your answers.  
- Be concise but specific — 2–4 sentences per cell is often enough.  
- This is **not a test prep sheet**. It’s a way to *document, reflect, and demonstrate* your process.

---

## Framework Guide Table

| Lifecycle Stage | What You Did | Challenges | Solutions / Decisions | Future Improvements |
|-----------------|--------------|------------|-----------------------|---------------------|
| **1. Problem Framing & Scoping** | *Defined the financial problem: predicting loan default using syntle success; limitehetic and real-world datasets. Goals were predictive accuracy, reproducibility, and explainability.* | *Balancing simplicity vs realism; defining measurabd initial domain knowledge.* | *Started with a clear target definition and baseline linear regression to frame expectations.* | *Explore multiple target definitions and include business KPIs earlier.* |
| **2. Tooling Setup** | *Configured Python environment, installed libraries (pandas, numpy, scikit-learn, matplotlib, streamlit).* | *Library version conflicts, kernel issues.* | *(Used a virtual environment and pinned versions in requirements.txt.* | *Automate environment setup with a script or Docker container.* |
| **3. Python Fundamentals** | *Applied Python for data cleaning, visualization, and model training. Used functions, classes, and modules for modularity.* | *Some gaps in handling large datasets efficiently.* | *Practiced vectorized operations, list comprehensions, and pandas best practices.* | *Strengthen knowledge of efficient pandas and NumPy operations.* |
| **4. Data Acquisition / Ingestion** | *Imported datasets from CSV, merged real and synthetic datasets.* | *Missing values, inconsistent formats, some ID mismatches.* | *Implemented a robust ingestion pipeline, standardized columns, validated schemas.* | *Add automated data validation and logging for future ingestion.)* |
| **5. Data Storage** | *Stored processed data in data/processed/; raw CSVs in data/raw/.* | *Ensuring reproducibility and avoiding accidental overwrites.* | *Used clear folder structure, versioned processed data files.* | *Consider lightweight database storage for larger datasets.* |
| **6. Data Preprocessing** | *Handled missing values, normalized numeric columns, dropped irrelevant ID columns.* | *Non-numeric columns caused errors in model training.* | *Dropped ID columns, optionally encoded categorical variables, standardized numerical features.* | *Automate preprocessing pipeline and add feature validation.* |
| **7. Outlier Analysis** | *Detected anomalies using descriptive statistics and visualization.* | *Hard to distinguish true outliers from rare but valid cases. | *Capped extreme values, kept business-relevant outliers.* | *Explore robust statistical techniques or model-based outlier detection.* |
| **8. Exploratory Data Analysis (EDA)** | *Visualized distributions, correlations, scatter plots, and summary statistics.* | *Some correlations were misleading due to skewed data.* | *Applied log transformations and visualized cleaned distributions.* | *Add interactive dashboards (Plotly/Streamlit) for more dynamic EDA.* |
| **9. Feature Engineering** | *Created ratios, lags, and interaction terms relevant to loan risk.* | *Features like age, basic_salary, and some engineered interaction terms showed weak predictive power according to feature importance and correlation analysis* | *Validated feature usefulness using feature importance and correlation analysis.* | *credit utilization ratio, employment length, number of existing loans, repayment history trends (e.g., missed payments last 6 months), and macroeconomic indicators such as inflation rate or interest rate changes* |
| **10. Modeling (Regression / Time Series / Classification)** | *Started with linear regression to establish a baseline model; then tried Random Forest regression to capture non-linear relationships and interactions in the data* | *Linear regression struggled with residuals and weak predictive power for certain features; Random Forest had longer training time and required careful feature handling* | *Chose final model based on cross-validation RMSE; tuned hyperparameters for Random Forest (n_estimators, max_depth) to balance bias-variance tradeoff* | *Gradient Boosting (XGBoost, LightGBM) or regularized linear models (Ridge, Lasso) to see if they improve predictive performance while maintaining interpretability.* |
| **11. Evaluation & Risk Communication** | *Evaluated RMSE, MAE, and R² on train/test splits.* | *Explaining error metrics to non-technical stakeholders.* | *Prepared clear metric summaries and visualizations to communicate risk.* | *Use prediction intervals and SHAP values for better interpretability.* |
| **12. Results Reporting, Delivery Design & Stakeholder Communication** | *Generated reports/summary.json, stakeholder PDF, and dashboard.* | *It was hard to explain why certain ratios (loan-to-income) mattered more than simple numeric features like age or disbursement amount, without overwhelming non-technical stakeholders with model internals* | *Simplified visualizations, highlighted actionable insights.* | ** |
| **13. Productization** | *Packaged model and preprocessing pipeline for reuse. Saved model with joblib.* | *Handling unseen feature inputs in predictions.* | *Implemented prepare_data() and input validation functions.* | *Add automated pipeline tests and versioned releases.* |
| **14. Deployment & Monitoring** | *Deployed Streamlit dashboard; prepared Flask API for predictions.* | *Ensuring feature alignment between training and runtime inputs.* | *Input validation and exception handling in API.* | *Add real-time monitoring, logging, and alerts for drift.* |
| **15. Orchestration & System Design** | *Integrated preprocessing, model training, and prediction into workflow.* | *Dependency order caused occasional runtime errors.* | *Modularized scripts, used functions to maintain order.* | *Explore workflow orchestration tools like Airflow or Prefect.* |
| **16. Lifecycle Review & Reflection** | *Reflected on project end-to-end: data acquisition → modeling → delivery. Learned importance of reproducibility, modular code, and stakeholder communication.* | *Biggest struggle: handling missing/erroneous data and aligning features between train/test/prediction.* | *Strategy: modular functions, pipeline checks, documentation, versioning.* | *Next project: automate pipeline, add more rigorous cross-validation, incorporate real-time data monitoring.* |

---

## Reflection Prompts

- Most difficult stage: Data preprocessing and outlier handling; ensuring feature consistency between training and prediction.  
- Most rewarding stage: Productization and deployment — seeing the model run in a dashboard for stakeholders.  
- Stage connections: Early decisions (feature selection, target definition) strongly constrained later modeling and evaluation stages.  
- Future improvements: Automate environment, preprocessing, and deployment; strengthen statistical feature validation.  
- Skills to strengthen: Python efficiency for large datasets, model interpretability techniques, pipeline orchestration.  

---