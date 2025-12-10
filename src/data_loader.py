import pandas as pd

def load_data(path):
    df = pd.read_csv(path)
    df = df.rename(columns={"Is Laundering": "Is_Laundering"})
    return df
