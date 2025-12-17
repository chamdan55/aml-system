from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from uuid import uuid4
from datetime import datetime

from kafka import producer
from services.common.schemas.transaction import Transaction
from services.common.settings import KAFKA_TOPIC_TRANSACTIONS
from services.backend.app.producer_service import ProducerService
producer_service = ProducerService()

app = FastAPI(title="AML Backend API")

@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/produce")
def produce(count: int = 1):
    produced = []

    for _ in range(count):
        tx = Transaction(
            transaction_id=str(uuid4()),
            from_account="acc_001",
            to_account="acc_999",
            amount=100000,
            currency="IDR",
            timestamp=datetime.utcnow(),
            metadata={"source": "fastapi-test"},
        )

        producer.send(
            KAFKA_TOPIC_TRANSACTIONS,
            value=tx.dict(),
        )

        produced.append(tx.transaction_id)

    return {
        "status": "sent",
        "count": len(produced),
        "transaction_ids": produced,
    }

# API
@app.post("/api/producer/start")
def start(rate: int = 5):
    started = producer_service.start(rate)
    return {"status": "started" if started else "already_running", "rate": rate}

@app.post("/api/producer/stop")
def stop():
    producer_service.stop()
    return {"status": "stopped"}

@app.get("/api/producer/status")
def status():
    return producer_service.status()

# Serve FE
app.mount("/ui", StaticFiles(directory="services/backend/static", html=True), name="static")