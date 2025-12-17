from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Optional

class Transaction(BaseModel):
    transaction_id: str
    from_account: str
    to_account: str
    amount: float
    currency: str = "IDR"
    timestamp: datetime

    channel: str
    country: str

    metadata: Optional[Dict] = Field(default_factory=dict)
