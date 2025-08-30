import pandas as pd

def add_loan_features(df):
    df['DebtToIncome'] = df['LoanAmount'] / df['Basic Salary']
    df['PrincipalPaidPct'] = (df['LoanAmount'] - df['PrincipalBalance']) / df['LoanAmount']
    df['HighSalaryFlag'] = (df['Basic Salary'] > df['Basic Salary'].quantile(0.75)).astype(int)
    return df
