-- Idempotent initialization for AML Postgres schema
-- Creates transactions_staging table and related indexes

CREATE TABLE IF NOT EXISTS transactions_staging (
  transaction_id TEXT PRIMARY KEY,
  from_account   TEXT NOT NULL,
  to_account     TEXT NOT NULL,
  amount         NUMERIC(18,2) NOT NULL,
  currency       TEXT NOT NULL,
  ts             TIMESTAMPTZ NOT NULL,
  channel        TEXT,
  country        TEXT,

  raw_object_key TEXT NOT NULL,
  ingested_at    TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_tx_ts ON transactions_staging (ts);
CREATE INDEX IF NOT EXISTS idx_tx_from_ts ON transactions_staging (from_account, ts);
CREATE INDEX IF NOT EXISTS idx_tx_to_ts ON transactions_staging (to_account, ts);
