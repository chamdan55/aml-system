from datetime import datetime
from uuid import uuid4
from services.backend.app.aml_patterns.base import AMLPattern
from services.common.schemas.transaction import Transaction

class FanOutPattern(AMLPattern):
    def generate(self):
        base_time = datetime.utcnow()
        txs = []

        for i in range(5):
            txs.append(
                Transaction(
                    transaction_id=str(uuid4()),
                    from_account="acc_fanout_A",
                    to_account=f"acc_fanout_{i}",
                    amount=500_000,
                    currency="IDR",
                    timestamp=base_time,
                    channel="web",
                    country="ID",
                    metadata={"pattern": "fan_out"}
                )
            )
        return txs
