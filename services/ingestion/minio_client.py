from minio import Minio
from services.common.settings import *

minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False,
)

if not minio_client.bucket_exists(MINIO_BUCKET_RAW):
    minio_client.make_bucket(MINIO_BUCKET_RAW)