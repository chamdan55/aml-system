import json
import asyncio
from kafka import KafkaConsumer
from datetime import datetime
from common.schemas.transaction import Transaction
from db import AsyncSessionLocal
from minio_client import minio_client
from services.common.settings import *

consumer = KafkaConsumer(
    KAFKA_TOPIC_TRANSACTIONS,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    group_id=KAFKA_GROUP_ID,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True,
)

async def persist_postgres(tx: Transaction):
    async with AsyncSessionLocal() as session:
        await session.execute(
            """
            INSERT INTO transactions_raw (transaction_id, payload)
            VALUES (:id, :payload)
            ON CONFLICT (transaction_id) DO NOTHING
            """,
            {
                "id": tx.transaction_id,
                "payload": tx.json(),
            },
        )
        await session.commit()

def persist_minio(tx: Transaction):
    key = f"transactions/{tx.transaction_id}.json"
    minio_client.put_object(
        MINIO_BUCKET_RAW,
        key,
        data=tx.json().encode(),
        length=len(tx.json()),
        content_type="application/json",
    )

print("AML Consumer started...")

loop = asyncio.get_event_loop()

for msg in consumer:
    tx = Transaction(**msg.value)

    loop.run_until_complete(persist_postgres(tx))
    persist_minio(tx)