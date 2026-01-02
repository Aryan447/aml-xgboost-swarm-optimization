from fastapi import APIRouter, HTTPException, Depends
import pandas as pd
from app.schemas.transaction import TransactionRequest, PredictionResponse
from app.services.model_service import ModelService
from app.core.config import settings

router = APIRouter()

# Dependency to get the model service
# We use a helper here to ensure it's loaded
def get_model_service():
    return ModelService(settings.MODEL_DIR)

@router.post("/predict", response_model=PredictionResponse)
def predict_transaction(
    txn: TransactionRequest,
    service: ModelService = Depends(get_model_service)
):
    try:
        # Convert Pydantic model to DataFrame (by_alias handles "From Bank" vs "from_bank")
        data = txn.dict(by_alias=True)
        df = pd.DataFrame([data])

        # Get prediction from service
        score = service.predict(df)

        return {
            "is_laundering": int(score > 0.5),
            "risk_score": round(score, 4),
            "risk_level": "CRITICAL" if score > 0.8 else "HIGH" if score > 0.5 else "LOW"
        }
    except RuntimeError as e:
        # Model not loaded
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        # General server error
        raise HTTPException(status_code=500, detail=str(e))
