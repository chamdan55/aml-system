# app/producer_service.py
import threading
import time
from datetime import datetime
from uuid import uuid4
from services.backend.app.kafka import producer
from services.common.schemas.transaction import Transaction
from services.common.settings import KAFKA_TOPIC_TRANSACTIONS

class ProducerService:
    def __init__(self):
        self._running = False
        self._thread = None
        self._sent = 0

    def _run(self, rate: int):
        interval = 1 / rate
        while self._running:
            tx = Transaction(
                transaction_id=str(uuid4()),
                from_account="acc_001",
                to_account="acc_999",
                amount=100000,
                currency="IDR",
                timestamp=datetime.utcnow(),
                channel="api",
                country="ID",
                metadata={"source": "backend-control"},
            )
            producer.send(KAFKA_TOPIC_TRANSACTIONS, value=tx.dict())
            self._sent += 1
            time.sleep(interval)

    def start(self, rate: int = 5):
        if self._running:
            return False
        self._running = True
        self._thread = threading.Thread(
            target=self._run, args=(rate,), daemon=True
        )
        self._thread.start()
        return True

    def stop(self):
        self._running = False
        return True

    def status(self):
        return {
            "running": self._running,
            "sent": self._sent,
        }

producer_service = ProducerService()