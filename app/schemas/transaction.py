from pydantic import BaseModel, Field

class TransactionRequest(BaseModel):
    timestamp: str = Field(..., alias="Timestamp", example="2022/09/01 08:30")
    from_bank: int = Field(..., alias="From Bank")
    account: str = Field(..., alias="Account")
    to_bank: int = Field(..., alias="To Bank")
    account_dest: str = Field(..., alias="Account.1")
    amount_received: float = Field(..., alias="Amount Received")
    receiving_currency: str = Field(..., alias="Receiving Currency")
    amount_paid: float = Field(..., alias="Amount Paid")
    payment_currency: str = Field(..., alias="Payment Currency")
    payment_format: str = Field(..., alias="Payment Format")

    class Config:
        populate_by_name = True

class PredictionResponse(BaseModel):
    is_laundering: int
    risk_score: float
    risk_level: str
