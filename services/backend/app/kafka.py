import json
from kafka import KafkaProducer
from services.common.settings import KAFKA_BOOTSTRAP_SERVERS


def json_serializer(data):
    return json.dumps(data, default=str).encode("utf-8")


producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=json_serializer,
    linger_ms=10,
)
