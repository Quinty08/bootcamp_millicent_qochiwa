\# Corporate Loan Credit Scoring Project



##\*\*Stage:\*\* Problem Framing \& Scoping (Stage 01)



\## Problem Statement

Commercial banks face challenges in assessing the creditworthiness of corporate borrowers, especially mid-sized firms without extensive credit histories. Current methods rely heavily on financial ratios and manual assessments, which are time-consuming and may overlook important predictive signals. A more systematic, data-driven approach is needed to reduce default risk and improve loan portfolio quality.



\## Stakeholder \& User

The primary stakeholder is the bank’s credit risk team (decision-makers), while the main users are credit analysts and loan officers who review applications and approve/reject loans. Their workflow requires timely, reliable scoring models that fit into existing risk review processes.



\## Useful Answer \& Decision

The project should deliver a \*\*predictive model\*\* that estimates the probability of default (PD) for corporate loans. The useful artifact is a scoring system or risk ranking metric that enables the bank to decide whether to approve, reject, or price a loan appropriately.



\## Assumptions \& Constraints

\- Assumes access to historical corporate loan data (features: affordability, payment history, industry info).

\- Must handle missing or incomplete borrower data.

\- Models need to be interpretable for regulators and credit committees.

\- Deployment must work within latency limits of loan review process.



\## Known Unknowns / Risks

\- Data quality issues (incomplete financial reporting).

\- Changing macroeconomic conditions affecting default risk.

\- Regulatory requirements for transparency in credit models.

\- Model drift over time as borrower behavior changes.



\## Lifecycle Mapping

| Goal | Stage | Deliverable |

|------|-------|-------------|

| Frame credit scoring problem | Problem Framing \& Scoping (Stage 01) | Scoping paragraph + repo setup |

| Build baseline predictive model | Modeling \& Evaluation (Stage 02) | Prototype notebook |

| Validate and interpret results | Evaluation \& Stress Testing (Stage 03) | Validation memo |

| Deliver stakeholder-facing tool | Deployment \& Handoff (Stage 04) | Risk scoring artifact |



\## Repo Plan

Folders: `/data/`, `/src/`, `/notebooks/`, `/docs/`


## Stage 02 — Tooling Setup

**Objective:**  
Establish a reproducible project environment, prepare folder structure, and ensure version control for all future stages.

**Folder Structure:**  
The project is organized for maintainability and clarity:


**Key Setup Items:**  
- `.gitignore` added to exclude temporary, OS, and sensitive files.  
- `requirements.txt` added to capture the Python environment (`bootcamp_env`) for reproducibility.  
- Initial scaffolding for `/data/`, `/docs/`, `/notebooks/`, `/src/`, and `/tests/` prepared.  

## Stage 03 — Python Fundamentals

**Objective:** Establish modular, reusable Python code for preprocessing and analysis.

**Deliverables:**
- `notebooks/python_fundamentals_summary.ipynb` — dummy data demonstrating Python, pandas, and NumPy operations.
- `src/utils.py` — reusable utility function(s) with documentation.

**Next Steps:**  
Use these utilities in future stages for data preprocessing, modeling, and EDA.

## Stage 04: Data Acquisition / Ingestion

**Raw data location:** `data/raw/xtenda_final.csv`  

**Data source:** Pre-collected dataset (XTENDA), anonymized for privacy.  
- Original IDs and employee names were replaced with `ID_#` and `Employee_#`.  
- Synthetic columns added: `Region`, `Gender`, `Age`.  

**Columns:**
- ID number
- Personnel Number
- Name of employee
- Basic Salary
- Payment
- AFFORDABILITY
- Loan_ID
- Region
- Gender
- Age

**Notes:**
- All identifiers anonymized to protect privacy.
- Dataset ready for ingestion and preprocessing in subsequent stages.

## Stage 05 Data Storage

Our project uses the following storage conventions:

- **data/raw/**: contains the original datasets exactly as obtained (e.g., `raw_loan_data.xlsx`, plus CSV and Parquet versions).
- **data/processed/**: contains intermediate and cleaned datasets prepared for modeling.

### File formats
- **Excel (.xlsx)**: original raw file
- **CSV (.csv)**: lightweight, portable version of raw and processed data
- **Parquet (.parquet)**: efficient binary format for large-scale processing

### Environment-driven paths
We use a `.env` file to define paths for data files. Example keys:

Never commit `.env`; instead, use `.env.example` for sharing path structure.

## Stage 06 – Data Preprocessing
Overview

In this stage, the project moves from raw data storage into data preprocessing. The goal is to clean, transform, and prepare the dataset so that it is ready for modeling in later stages.

The preprocessing pipeline was designed to be modular and reusable, with functions stored in src/cleaning.py and demonstrated in a Jupyter notebook.

Preprocessing Steps

Loading Raw Data

The raw loan dataset is loaded from the /data/raw/ directory.

File paths are managed through environment variables defined in .env.example to ensure portability.

Handling Missing Values

Columns such as Tenure, LoanDate, DisbursementAmount, LastPaymentDate, PrincipalBalance, LoanStatus, InterestRate, LoanPurpose, RetirementDate, and IsNPL contained missing values.

Missing value strategies:

Numeric columns (e.g., LoanAmount, Instalment, PrincipalBalance): imputed using median values or left as NaN where business meaning requires.

Categorical columns (e.g., LoanStatus, Regions, LoanPurpose): imputed using mode or flagged as "Unknown".

Date columns (e.g., LoanDate, DisbursementDate, LastPaymentDate): parsed into datetime objects, missing entries flagged for further review.

Data Type Conversion

Converted salary, payment, and loan amounts to numeric.

Converted date columns into proper datetime objects.

Converted categorical fields (Gender, Regions, LoanStatus, LoanPurpose) to categorical data types for efficiency.

Feature Engineering

Derived additional features such as:

Debt-to-Income Ratio (DTI) = Instalment / Basic Salary.

Loan Age = difference between today’s date and LoanDate.

These features will support downstream modeling tasks.

Saving Processed Data

The cleaned dataset is saved to /data/processed/processed_loans.csv and /data/processed/processed_loans.parquet.

This ensures a reproducible, consistent version of the dataset for all teammates.

Assumptions & Rationale

Blank values in loan-related columns represent incomplete loan history rather than errors; imputation was done conservatively.

Salary and payment fields are assumed to be monthly values.

Loan IDs are unique identifiers and not altered.

Gender, Regions, and LoanStatus values outside expected categories were grouped into "Unknown" for consistency.

Dates with missing values were not forward/backward filled since doing so would introduce artificial patterns into loan timelines.


##Stage 07 – Outlier Analysis

Definition used:
An observation is an outlier in a given numeric feature if it lies outside the IQR rule:

[Q1−1.5×IQR,Q3+1.5×IQR]

Columns considered:
All numeric columns except identifiers (e.g., Personnel Number). This avoids treating keys as outliers.

Two strategies implemented (see src/outliers.py):

winsorize_iqr(...) – Caps extreme values to the IQR bounds (keeps all rows, reduces influence).

remove_outliers_iqr(...) – Drops rows that have any outlier (more aggressive).

Sensitivity notebook: notebooks/sensitivity_outliers.ipynb

Generates a per-column outlier summary.

Saves two variants to data/processed/:

cleaned_loan_data_capped.csv (17,719 rows, all retained)

cleaned_loan_data_trimmed.csv (10,333 rows after trimming ≈42% reduction)

Compares summary statistics (mean, median, std, skew) before vs after treatment.

Observed effects:

Winsorization reduced skewness for heavy-tailed variables (e.g., Salary, LoanAmount, Payment).

Trimming further tightened distributions but at the cost of losing ~6,300 rows.

Some variables (Age, Tenure) showed little change since they were already within reasonable bounds.

Assumptions & Rationale:

Credit-related variables (salary, payment, loan amount, principal balance, interest rate, age, tenure) are often heavy-tailed.

We default to winsorization to preserve sample size while limiting leverage of extreme values.

Trimming is provided for sensitivity analysis; final choice will depend on downstream model performance and fairness checks.

Risks:

Some extreme values may be legitimate (e.g., very large corporate loans); capping could bias tail behavior.

Dropping outliers may remove critical edge cases (e.g., actual defaults at extremes).

We will review feature distributions and model metrics before locking in the final policy.


##Stage 09 – Feature Engineering

Features Created:

1. DebtToIncome

Definition: LoanAmount / Basic Salary

Rationale: Represents the borrower's debt burden relative to income. High ratios indicate higher risk of default.

Use in Models: Helps predictive models assess financial stress and creditworthiness.

2. PrincipalPaidPct

Definition: (LoanAmount - PrincipalBalance) / LoanAmount

Rationale: Measures the proportion of the loan that has already been repaid.

Use in Models: Provides insight into repayment behavior and loan progress; may correlate with default probability.

3. HighSalaryFlag

Definition: 1 if Basic Salary > 75th percentile, else 0

Rationale: Flags borrowers with above-median income, who may have lower default risk.

Use in Models: Supports segmentation and risk differentiation in predictive modeling.

Implementation:

All features were added via the function add_loan_features(df) in /src/feature_engineering.py.

The resulting dataset with engineered features is saved as /data/processed/loan_data_features.csv.

Assumptions & Notes:

DebtToIncome assumes salary is a reliable measure of income and is not zero.

PrincipalPaidPct assumes no negative balances or loan cancellations.

HighSalaryFlag uses the 75th percentile as a threshold; this can be adjusted depending on business rules or modeling needs.

Next Steps:

These features will be used in subsequent modeling stages for risk assessment and predictive analytics.

Additional features may be created after further domain analysis or model diagnostics.


## Stage 10a – Modeling (Regression)

**Target:** `AFFORDABILITY` (numeric).

**Split:** Time-aware split on `LoanDate` (last 20% used as test). Falls back to random split if `LoanDate` missing.

**Features:** All numeric and categorical columns except identifiers and date fields; includes engineered features from Stage 09 (e.g., `DebtToIncome`, `PrincipalPaidPct`, `HighSalaryFlag`).

**Pipelines:** Preprocessing via `ColumnTransformer` (StandardScaler for numeric, One-Hot for categorical), then model.

**Models tried:** 
- Linear Regression  
- RidgeCV  
- LassoCV  
- RandomForestRegressor  

**Evaluation:** Metrics reported on the test set: MAE, RMSE, R².  
- RandomForest performed best (MAE ~108, RMSE ~316, R² ≈ 0.97).  
- Linear, Ridge, and Lasso were similar (MAE ~172, RMSE ~361, R² ≈ 0.963).  
- Regularization (Ridge/Lasso) did not yield major gains over plain Linear Regression.

**Rationale:** Start with a simple linear baseline for interpretability, check regularized versions for stability, and benchmark against a non-linear tree ensemble. RandomForest provided a significant performance boost, showing the presence of non-linear relationships.  


tage 10b – Modeling (Regression) with Diagnostics

Target: AFFORDABILITY (numeric)

Train-Test Split: Time-aware on LoanDate (last 20% as test set)

Features:

All numeric and categorical features except identifiers and date columns

Includes engineered features from Stage 09: DebtToIncome, PrincipalPaidPct, HighSalaryFlag

Models Tried:

Linear Regression

RidgeCV

LassoCV

RandomForestRegressor

Evaluation Metrics (Test Set):

Model	MAE	RMSE	R²
Linear	172.27	360.66	0.963
RidgeCV	172.57	360.77	0.963
LassoCV	171.38	361.39	0.963
RandomForest	108.56	314.13	0.972

Residual Analysis (Linear Regression):

Residuals vs Fitted plot shows residuals roughly centered around zero; no clear trend → homoscedasticity is reasonable.

QQ plot indicates residuals approximately follow a normal distribution, supporting linear regression assumptions.

Some extreme residuals exist (outliers), consistent with heavy-tailed financial data.

Rationale & Next Steps:

Linear regression provides interpretability and baseline performance.

RandomForest improves predictive accuracy, especially for extreme cases, but loses coefficient interpretability.

Stage 10b confirms that our features and preprocessing are suitable for regression modeling.

Future improvements: consider robust regression or additional transformations to handle tail behavior and extreme residuals.


##Stage 11 — Evaluation & Risk Communication

What we evaluated

Models: Linear Regression and RandomForest.

Imputation strategies: mean vs. median for missing values.

Metrics: MAE, RMSE (manual sqrt of MSE), R².

Uncertainty quantification: Bootstrap 95% confidence intervals for MAE.

Subgroup diagnostics: performance per region to check fairness/consistency.

Key results

RandomForest (mean imputation) performed best (lowest MAE & RMSE).

Linear regression remains more interpretable but had higher error.

Bootstrap confidence intervals highlight uncertainty ranges; overlapping CIs may suggest results are not statistically distinct.

Subgroup results showed variation across regions, suggesting the need for fairness checks.

Assumptions & risks

Results depend on how missing values are imputed.

Identifier-like columns were removed to prevent data leakage.

Model performance could degrade under outliers or shifted input distributions.

Next steps

Run fairness and stress tests (especially for high-risk inputs).

Monitor prediction distributions, feature drift, and subgroup accuracy in production.

Plan retraining cadence and document productionization steps.

Files

notebooks/stage11_evaluation.ipynb — evaluation code and plots.

outputs/ — saved pipelines, summary (stage11_summary.txt), and metrics CSV.


