# app/producer_service.py
import threading
import time
from datetime import datetime
from uuid import uuid4
from services.backend.app.kafka import producer
from services.common.schemas.transaction import Transaction
from services.common.settings import KAFKA_TOPIC_TRANSACTIONS
from services.backend.app.aml_patterns.normal import NormalFlow
from services.backend.app.aml_patterns.smurfing import SmurfingPattern
from services.backend.app.aml_patterns.fanout import FanOutPattern
from services.backend.app.aml_patterns.layering import LayeringCyclePattern

PATTERNS = {
    "normal": NormalFlow(),
    "smurfing": SmurfingPattern(),
    "fanout": FanOutPattern(),
    "layering": LayeringCyclePattern(),
}
LOOP_PATTERN = {
    "normal": "smurfing",
    "smurfing": "fanout",
    "fanout": "layering",
    "layering": "normal",
}


class ProducerService:
    def __init__(self):
        self._running = False
        self._thread = None
        self._sent = 0
        self._current_pattern = "normal"

    def _run(self, rate: int):
        interval = 1 / rate
        while self._running:
            pattern = self._current_pattern
            for tx in PATTERNS[pattern].generate():
                producer.send(KAFKA_TOPIC_TRANSACTIONS, value=tx.dict())
                self._sent += 1
            
            self._current_pattern = LOOP_PATTERN[pattern]
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