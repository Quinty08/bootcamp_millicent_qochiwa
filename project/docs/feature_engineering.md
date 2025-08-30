**Stage 09 – Feature Engineering**



Features Created:



1. DebtToIncome



Definition: LoanAmount / Basic Salary



Rationale: Represents the borrower's debt burden relative to income. High ratios indicate higher risk of default.



Use in Models: Helps predictive models assess financial stress and creditworthiness.



2\. PrincipalPaidPct



Definition: (LoanAmount - PrincipalBalance) / LoanAmount



Rationale: Measures the proportion of the loan that has already been repaid.



Use in Models: Provides insight into repayment behavior and loan progress; may correlate with default probability.



3\. HighSalaryFlag



Definition: 1 if Basic Salary > 75th percentile, else 0



Rationale: Flags borrowers with above-median income, who may have lower default risk.



Use in Models: Supports segmentation and risk differentiation in predictive modeling.



Implementation:



All features were added via the function add\_loan\_features(df) in /src/feature\_engineering.py.



The resulting dataset with engineered features is saved as /data/processed/loan\_data\_features.csv.



Assumptions \& Notes:



DebtToIncome assumes salary is a reliable measure of income and is not zero.



PrincipalPaidPct assumes no negative balances or loan cancellations.



HighSalaryFlag uses the 75th percentile as a threshold; this can be adjusted depending on business rules or modeling needs.



**Next Steps:**



These features will be used in subsequent modeling stages for risk assessment and predictive analytics.



Additional features may be created after further domain analysis or model diagnostics.

