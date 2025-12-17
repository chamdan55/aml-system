KAFKA_BOOTSTRAP_SERVERS="kafka:29092"
KAFKA_TOPIC_TRANSACTIONS="transactions"
KAFKA_GROUP_ID = "aml-consumer-raw"

DATABASE_URL = "postgresql+asyncpg://aml:aml@aml_postgres:5432/aml"

MINIO_ENDPOINT="minio:9000"
MINIO_ACCESS_KEY="minioadmin"
MINIO_SECRET_KEY="minioadmin"
MINIO_BUCKET_RAW="aml-raw"