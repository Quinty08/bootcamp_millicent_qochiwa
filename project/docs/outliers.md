Stage 07 – Outlier Analysis



Definition used:

An observation is an outlier in a given numeric feature if it lies outside the IQR rule:



\[Q1−1.5×IQR,Q3+1.5×IQR]



**Columns considered:**

All numeric columns except identifiers (e.g., Personnel Number). This avoids treating keys as outliers.



Two strategies implemented (see src/outliers.py):



winsorize\_iqr(...) – Caps extreme values to the IQR bounds (keeps all rows, reduces influence).



remove\_outliers\_iqr(...) – Drops rows that have any outlier (more aggressive).



Sensitivity notebook: notebooks/sensitivity\_outliers.ipynb



Generates a per-column outlier summary.



Saves two variants to data/processed/:



cleaned\_loan\_data\_capped.csv (17,719 rows, all retained)



cleaned\_loan\_data\_trimmed.csv (10,333 rows after trimming ≈42% reduction)



Compares summary statistics (mean, median, std, skew) before vs after treatment.



**Observed effects:**



Winsorization reduced skewness for heavy-tailed variables (e.g., Salary, LoanAmount, Payment).



Trimming further tightened distributions but at the cost of losing ~6,300 rows.



Some variables (Age, Tenure) showed little change since they were already within reasonable bounds.



Assumptions \& Rationale:



Credit-related variables (salary, payment, loan amount, principal balance, interest rate, age, tenure) are often heavy-tailed.



We default to winsorization to preserve sample size while limiting leverage of extreme values.



Trimming is provided for sensitivity analysis; final choice will depend on downstream model performance and fairness checks.



**Risks**:



Some extreme values may be legitimate (e.g., very large corporate loans); capping could bias tail behavior.



Dropping outliers may remove critical edge cases (e.g., actual defaults at extremes).



We will review feature distributions and model metrics before locking in the final policy.

