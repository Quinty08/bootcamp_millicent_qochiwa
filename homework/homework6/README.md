\## Data Cleaning Strategy



For Homework 6, the raw dataset contained missing values in several numeric columns and needed preprocessing. The following steps were applied:



1\. \*\*Filling Missing Values\*\*

&nbsp;  - Numeric columns with missing values were filled using the \*\*median\*\*:

&nbsp;    - `age`: median = 39.5

&nbsp;    - `income`: median = 52000

&nbsp;    - `score`: median = 0.805

&nbsp;    - `extra\_data`: median = 23.5

&nbsp;  - This ensures no numeric column contains `NaN` values after cleaning.



2\. \*\*Dropping Rows with Too Many Missing Values\*\*

&nbsp;  - Rows with more than \*\*50% missing values\*\* would be dropped using a threshold-based function.

&nbsp;  - In this dataset, \*\*no rows were dropped\*\* because all rows had ≤50% missing values.



3\. \*\*Normalization\*\*

&nbsp;  - Numeric columns (`age`, `income`, `score`, `extra\_data`) were scaled to a \*\*0–1 range\*\* using Min-Max normalization.

&nbsp;  - Non-numeric columns (`zipcode`, `city`) were not modified.



4\. \*\*Outcome\*\*

&nbsp;  - The cleaned dataset has \*\*no missing values\*\* and all numeric columns are normalized.

&nbsp;  - The dataset is saved to `data/processed/sample\_data\_cleaned.csv` and is ready for analysis or modeling.



\*\*Assumptions Made:\*\*

\- Median is an appropriate replacement for missing numeric values.

\- No categorical columns required encoding or transformation.

\- Rows with less than 50% missing values are preserved to retain as much data as possible.



