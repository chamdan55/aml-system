# services/ingestion/schemas.py
from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime


class Transaction(BaseModel):
    transaction_id: str
    from_account: str
    to_account: str
    amount: float
    currency: str = "IDR"
    timestamp: datetime
    channel: str
    country: str
    metadata: Optional[Dict] = {}
