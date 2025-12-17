import json
from datetime import datetime
from minio import Minio
import asyncpg
import asyncio
import os
from services.common.schemas.transaction import Transaction
from services.common.settings import *
from services.ingestion.minio_client import minio_client

# Prefer DATABASE_URL from environment if provided; fallback to settings
DATABASE_URL = os.getenv("DATABASE_URL", DATABASE_URL)

minio = minio_client

async def upsert_tx(pool, tx: Transaction, raw_key: str):
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO transactions_staging (
              transaction_id, from_account, to_account, amount, currency,
              ts, channel, country, raw_object_key
            )
            VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9)
            ON CONFLICT (transaction_id) DO NOTHING
            """,
            tx.transaction_id,
            tx.from_account,
            tx.to_account,
            tx.amount,
            tx.currency,
            tx.timestamp,
            tx.channel,
            tx.country,
            raw_key,
        )

async def main():
    pool = await asyncpg.create_pool(DATABASE_URL)

    # iterate RAW objects (simple scan; later bisa incremental)
    objects = minio.list_objects(
        MINIO_BUCKET_RAW,
        prefix="transactions/",
        recursive=True
    )

    async for obj in _aiter(objects):
        resp = minio.get_object(MINIO_BUCKET_RAW, obj.object_name)
        payload = json.loads(resp.read().decode())
        resp.close(); resp.release_conn()

        tx = Transaction(**payload)
        await upsert_tx(pool, tx, obj.object_name)

    await pool.close()

async def _aiter(it):
    for x in it:
        yield x

if __name__ == "__main__":
    asyncio.run(main())
