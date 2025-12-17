import json
import logging
from datetime import datetime
from minio import Minio
import asyncpg
import asyncio
import os
from services.common.schemas.transaction import Transaction
from services.common.settings import *
from services.ingestion.minio_client import minio_client

PIPELINE_NAME = "raw_to_staging_transactions"

# Prefer DATABASE_URL from environment if provided; fallback to settings
DATABASE_URL = os.getenv("DATABASE_URL", DATABASE_URL)

minio = minio_client

async def already_processed(conn, object_key: str) -> bool:
    row = await conn.fetchrow(
        """
        SELECT 1 FROM etl_checkpoints
        WHERE pipeline_name = $1 AND object_key = $2
        """,
        PIPELINE_NAME,
        object_key,
    )
    return row is not None

async def mark_processed(conn, object_key: str):
    await conn.execute(
        """
        INSERT INTO etl_checkpoints (pipeline_name, object_key)
        VALUES ($1, $2)
        ON CONFLICT DO NOTHING
        """,
        PIPELINE_NAME,
        object_key,
    )

async def insert_staging(conn, tx: Transaction, object_key: str):
    await conn.execute(
        """
        INSERT INTO transactions_staging (
          transaction_id, from_account, to_account,
          amount, currency, ts, channel, country,
          raw_object_key
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
        object_key,
    )

async def main():
    # Track how many objects we store in this run
    stored_count = 0
    skipped_count = 0

    pool = await asyncpg.create_pool(DATABASE_URL)

    objects = minio.list_objects(
        MINIO_BUCKET_RAW,
        prefix="transactions/",
        recursive=True,
    )

    async with pool.acquire() as conn:
        async for obj in _aiter(objects):
            if await already_processed(conn, obj.object_name):
                skipped_count += 1
                continue

            resp = minio.get_object(MINIO_BUCKET_RAW, obj.object_name)
            payload = json.loads(resp.read().decode())
            resp.close(); resp.release_conn()

            tx = Transaction(**payload)

            await insert_staging(conn, tx, obj.object_name)
            await mark_processed(conn, obj.object_name)
            stored_count += 1

    await pool.close()
    logging.info(
        "ETL %s: stored %d, skipped %d (already processed)",
        PIPELINE_NAME,
        stored_count,
        skipped_count,
    )

async def _aiter(it):
    for x in it:
        yield x

if __name__ == "__main__":
    # Ensure INFO logs are visible when running this script directly
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
