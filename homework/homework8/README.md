

\## Key Steps in the Notebook

1\. \*\*Data Loading \& Structure Check\*\*  

&nbsp;  - `.info()`, missing values, data types, basic sanity checks.



2\. \*\*Numeric Profiling\*\*  

&nbsp;  - `.describe()`, skewness, kurtosis for numeric columns.



3\. \*\*Distributions\*\*  

&nbsp;  - Histograms/KDEs for income, spend, transactions.  

&nbsp;  - Boxplots to identify outliers.



4\. \*\*Relationships\*\*  

&nbsp;  - Scatterplots for income vs spend, age vs spend, transactions vs spend, age vs income.  

&nbsp;  - Pairplot for all numeric features.



5\. \*\*Correlation Analysis\*\*  

&nbsp;  - Correlation matrix visualized using a heatmap to identify linear relationships.



6\. \*\*Insights \& Assumptions\*\*  

&nbsp;  - Top insights from distributions and relationships.  

&nbsp;  - Assumptions about missingness, skew, outliers, and regional differences.



7\. \*\*Next Steps\*\*  

&nbsp;  - Cleaning (imputation, outlier handling), transformations (log for skewed variables), and feature engineering (interaction terms, categorical encoding).



\## Top 3 Insights

1\. Income has a moderate positive correlation with spend, while age shows weak correlation with both income and spend.

2\. Transactions show the strongest positive correlation with spend, suggesting that activity level is a major driver.   

3\. Age has weak correlation with spend or income.



\## Assumptions \& Risks

\- Missing values may bias results.  

\- Outliers could distort statistical summaries.  

\- Regional differences may require categorical encoding.  

\- Skewed distributions need transformations for linear models.



\## Next Steps

\- Impute missing values, handle outliers, log-transform skewed features.  

\- Engineer interaction terms and encode categorical variables.  

\- Re-evaluate distributions and correlations post-cleaning.



---





