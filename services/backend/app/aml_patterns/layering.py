from datetime import datetime, timedelta
from uuid import uuid4
from services.backend.app.aml_patterns.base import AMLPattern
from services.common.schemas.transaction import Transaction

class LayeringCyclePattern(AMLPattern):
    def generate(self):
        t0 = datetime.utcnow()
        accounts = ["acc_L1", "acc_L2", "acc_L3"]

        return [
            Transaction(
                transaction_id=str(uuid4()),
                from_account=accounts[0],
                to_account=accounts[1],
                amount=1_000_000,
                currency="IDR",
                timestamp=t0,
                channel="mobile",
                country="ID",
                metadata={"pattern": "layering"}
            ),
            Transaction(
                transaction_id=str(uuid4()),
                from_account=accounts[1],
                to_account=accounts[2],
                amount=980_000,
                currency="IDR",
                timestamp=t0 + timedelta(seconds=30),
                channel="mobile",
                country="ID",
                metadata={"pattern": "layering"}
            ),
            Transaction(
                transaction_id=str(uuid4()),
                from_account=accounts[2],
                to_account=accounts[0],
                amount=960_000,
                currency="IDR",
                timestamp=t0 + timedelta(seconds=60),
                channel="mobile",
                country="ID",
                metadata={"pattern": "layering"}
            ),
        ]
