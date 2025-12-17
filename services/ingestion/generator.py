# services/ingestion/generator.py
import random
import uuid
from datetime import datetime, timedelta
from typing import List
from common.schemas.transaction import Transaction


CHANNELS = ["mobile", "web", "atm"]
COUNTRIES = ["ID", "SG", "MY", "PH"]
CURRENCY = "IDR"


class TransactionGenerator:
    def __init__(
        self,
        n_accounts: int = 1000,
        suspicious_ratio: float = 0.15,
    ):
        self.accounts = [f"acc_{i:05d}" for i in range(n_accounts)]
        self.suspicious_ratio = suspicious_ratio

    def _normal_transaction(self) -> Transaction:
        from_acc, to_acc = random.sample(self.accounts, 2)
        amount = round(random.uniform(10_000, 5_000_000), 2)

        return Transaction(
            transaction_id=str(uuid.uuid4()),
            from_account=from_acc,
            to_account=to_acc,
            amount=amount,
            currency=CURRENCY,
            timestamp=datetime.utcnow(),
            channel=random.choice(CHANNELS),
            country="ID",
            metadata={"type": "normal"},
        )

    def _suspicious_transaction(self) -> List[Transaction]:
        """
        Simulate fan-out / layering pattern
        """
        root_account = random.choice(self.accounts)
        targets = random.sample(self.accounts, random.randint(5, 15))
        base_amount = random.uniform(20_000_000, 100_000_000)

        txs = []
        for tgt in targets:
            txs.append(
                Transaction(
                    transaction_id=str(uuid.uuid4()),
                    from_account=root_account,
                    to_account=tgt,
                    amount=round(base_amount / len(targets), 2),
                    currency=CURRENCY,
                    timestamp=datetime.utcnow(),
                    channel=random.choice(CHANNELS),
                    country=random.choice(COUNTRIES),
                    metadata={"type": "suspicious", "pattern": "fan_out"},
                )
            )
        return txs

    def generate(self) -> List[Transaction]:
        if random.random() < self.suspicious_ratio:
            return self._suspicious_transaction()
        else:
            return [self._normal_transaction()]
