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






