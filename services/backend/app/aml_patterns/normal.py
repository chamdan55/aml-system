from datetime import datetime
from uuid import uuid4
from services.backend.app.aml_patterns.base import AMLPattern
from services.common.schemas.transaction import Transaction

class NormalFlow(AMLPattern):
    def generate(self):
        return [
            Transaction(
                transaction_id=str(uuid4()),
                from_account="acc_norm_01",
                to_account="acc_norm_02",
                amount=150_000,
                currency="IDR",
                timestamp=datetime.utcnow(),
                channel="mobile",
                country="ID",
                metadata={"pattern": "normal"}
            )
        ]
