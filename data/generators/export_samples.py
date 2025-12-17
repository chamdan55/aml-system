import pandas as pd
from datetime import datetime

data = [
    {
        "transaction_id": "tx_0001",
        "from_account": "acc_001",
        "to_account": "acc_002",
        "amount": 50000,
        "currency": "IDR",
        "timestamp": datetime.fromisoformat("2025-01-14T01:00:00"),
        "channel": "mobile",
        "country": "ID",
        "pattern": "normal"
    },
    {
        "transaction_id": "tx_0002",
        "from_account": "acc_001",
        "to_account": "acc_003",
        "amount": 75000,
        "currency": "IDR",
        "timestamp": datetime.fromisoformat("2025-01-14T01:01:10"),
        "channel": "mobile",
        "country": "ID",
        "pattern": "fan_out"
    },
    {
        "transaction_id": "tx_0003",
        "from_account": "acc_010",
        "to_account": "acc_020",
        "amount": 9500000,
        "currency": "IDR",
        "timestamp": datetime.fromisoformat("2025-01-14T02:15:45"),
        "channel": "branch",
        "country": "ID",
        "pattern": "high_value"
    }
]

df = pd.DataFrame(data)

df.to_csv("data/samples/transactions_sample.csv", index=False)
df.to_parquet("data/samples/transactions_sample.parquet", index=False)

print("Sample CSV & Parquet generated.")