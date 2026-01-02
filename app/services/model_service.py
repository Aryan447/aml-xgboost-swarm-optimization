import os
import joblib
import xgboost as xgb
import pandas as pd
import numpy as np

class ModelService:
    def __init__(self, model_dir: str):
        self.model = None
        self.scaler = None
        self.features = None
        self._load_artifacts(model_dir)

    def _load_artifacts(self, model_dir: str):
        try:
            print(f"Loading models from {model_dir}...")
            model_path = os.path.join(model_dir, "best_model_gwo.json")
            scaler_path = os.path.join(model_dir, "scaler.pkl")
            features_path = os.path.join(model_dir, "feature_columns.pkl")

            if not os.path.exists(model_path):
                raise FileNotFoundError(f"Model not found at {model_path}")

            self.model = xgb.Booster()
            self.model.load_model(model_path)
            self.scaler = joblib.load(scaler_path)
            self.features = joblib.load(features_path)
            print("✅ Models loaded successfully.")
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            # In production, you might want to crash here if models are critical

    def predict(self, input_df: pd.DataFrame) -> float:
        if not self.model:
            raise RuntimeError("Model service is not initialized.")

        # 1. Preprocess (Simplified for demo - align with training logic)
        # Timestamp
        if 'Timestamp' in input_df.columns:
            try:
                input_df['Timestamp'] = pd.to_datetime(input_df['Timestamp']).astype(int) / 10**9
            except:
                input_df['Timestamp'] = 0.0

        # Payment Mapping
        pay_map = {'Cash':1, 'Cheque':2, 'ACH':3, 'Credit Card':4,
                   'Wire':5, 'Bitcoin':6, 'Reinvestment':7}
        if 'Payment Format' in input_df.columns:
            input_df['Payment Format'] = input_df['Payment Format'].map(pay_map).fillna(0)

        # 2. Align Columns
        df_ready = pd.DataFrame(columns=self.features)
        for col in self.features:
            df_ready[col] = input_df[col] if col in input_df.columns else 0

        # 3. Scale & Predict
        data_scaled = self.scaler.transform(df_ready)
        dmatrix = xgb.DMatrix(data_scaled, feature_names=self.features)

        return float(self.model.predict(dmatrix)[0])
