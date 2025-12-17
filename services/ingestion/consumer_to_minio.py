import json
from io import BytesIO
from kafka import KafkaConsumer
from datetime import datetime
from minio import Minio
from services.common.settings import (
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_TOPIC_TRANSACTIONS,
    MINIO_ENDPOINT,
    MINIO_ACCESS_KEY,
    MINIO_SECRET_KEY,
    MINIO_BUCKET_RAW,
)

# Kafka Consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC_TRANSACTIONS,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="raw-landing-group",
)

# MinIO Client
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False,
)

# Ensure bucket exists
if not minio_client.bucket_exists(MINIO_BUCKET_RAW):
    minio_client.make_bucket(MINIO_BUCKET_RAW)

print("🚀 Consumer started. Writing raw data to MinIO...")

for msg in consumer:
    tx = msg.value
    ts = datetime.fromisoformat(tx["timestamp"].replace("Z", ""))

    object_name = (
        f"transactions/"
        f"date={ts.date()}/"
        f"{tx['transaction_id']}.json"
    )

    payload = json.dumps(tx).encode("utf-8")

    minio_client.put_object(
        bucket_name=MINIO_BUCKET_RAW,
        object_name=object_name,
        data=BytesIO(payload),
        length=len(payload),
        content_type="application/json",
    )

    print(f"📝 Stored {object_name}")
