import pandas as pd
import numpy as np

def load_raw_data(path:str) -> pd.DataFrame:
    return pd.read_csv(path)

def clean_loans(df:pd.DataFrame) -> pd.DataFrame:
    #Handle missing tenure
    df['Tenure'] = df['Tenure'].fillna(0)
   
    date_cols =['LoanDate', 'DisbursementDate', 'LastPaymentDate', 'RetirementDate']
    for col in date_cols:
        df[col]=pd.to_datetime(df[col], errors='coerce')

    #loan amount,disbursement amount, principal
    df['LoanAmount'] =  df['LoanAmount'].fillna(0)    
    df['DisbursementAmount'] =  df['DisbursementAmount'].fillna(0)    
    df['Instalment'] = df['Instalment'].fillna(0)
    df['PrincipalBalance'] = df['PrincipalBalance'].fillna(0)

    # --- Loan Status & Purpose ---
    df['LoanStatus']=df['LoanStatus'].fillna('Unknown')
    df['LoanPurpose'] = df['LoanPurpose'].fillna('Unknown')

    #Interest rate
    median_rate=df['InterestRate'].median()
    df['InterestRate'] =df['InterestRate'].fillna(median_rate)

    # --- IsNPL (Target variable) ---
    df= df.dropna(subset=['IsNPL'])
  
    return df

def save_processed_data(df:pd.DataFrame, path : str):
    df.to_csv(path, index=False)
    


