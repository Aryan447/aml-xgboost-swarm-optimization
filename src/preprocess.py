import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
import joblib

def preprocess_data(df):
    # Encode categorical
    object_cols = df.select_dtypes(include=['object']).columns.tolist()
    label_encoder = LabelEncoder()

    for col in object_cols:
        if col != 'Payment Format':
            df[col] = label_encoder.fit_transform(df[col])

    payment_map = {'Cash':1,'Cheque':2,'ACH':3,'Credit Card':4,'Wire':5,'Bitcoin':6,'Reinvestment':7}
    df['Payment Format'] = df['Payment Format'].map(payment_map)

    # Timestamp to numeric
    df['Timestamp'] = pd.to_datetime(df['Timestamp']).astype(int) / 10**9

    # Normalize
    labels = df['Is_Laundering']
    df = df.drop('Is_Laundering', axis=1)

    scaler = MinMaxScaler(feature_range=(-1,1))
    df_scaled = scaler.fit_transform(df)
    df_scaled = pd.DataFrame(df_scaled, columns=df.columns)
    df_scaled["Is_Laundering"] = labels

    return df_scaled, scaler

# Data Balance

def balance_data(df):
    df = df.sample(frac=1)
    fraud = df[df["Is_Laundering"] == 1]
    non_fraud = df[df["Is_Laundering"] == 0][:len(fraud)]
    balanced = pd.concat([fraud, non_fraud]).sample(frac=1, random_state=42)
    return balanced
