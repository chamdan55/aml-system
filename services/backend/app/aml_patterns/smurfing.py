from datetime import datetime, timedelta
from uuid import uuid4
from services.backend.app.aml_patterns.base import AMLPattern
from services.common.schemas.transaction import Transaction

class SmurfingPattern(AMLPattern):
    def generate(self):
        base_time = datetime.utcnow()
        txs = []

        for i in range(5):
            txs.append(
                Transaction(
                    transaction_id=str(uuid4()),
                    from_account="acc_smurf_A",
                    to_account="acc_smurf_B",
                    amount=9_900_000,  # di bawah threshold
                    currency="IDR",
                    timestamp=base_time + timedelta(seconds=i * 20),
                    channel="mobile",
                    country="ID",
                    metadata={"pattern": "smurfing"}
                )
            )
        return txs
