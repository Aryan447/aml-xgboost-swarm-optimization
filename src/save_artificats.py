import joblib
import os

def save_artifacts(model, scaler, columns):
    os.makedirs("models", exist_ok=True)

    model.save_model("models/best_model_gwo.json")
    joblib.dump(scaler, "models/scaler.pkl")
    joblib.dump(columns, "models/feature_columns.pkl")

    print("Saved model + scaler + feature columns!")
