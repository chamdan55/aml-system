# services/ingestion/producer.py
import json
import time
import argparse
from kafka import KafkaProducer
from generator import TransactionGenerator


def json_serializer(data):
    return json.dumps(data, default=str).encode("utf-8")


def main(rate: int):
    producer = KafkaProducer(
        bootstrap_servers="localhost:9092",
        value_serializer=json_serializer,
        linger_ms=10,
    )

    generator = TransactionGenerator()

    print("🚀 Starting transaction producer...")
    print(f"➡️  Rate: ~{rate} tx/sec")

    try:
        while True:
            tx_batch = generator.generate()
            for tx in tx_batch:
                producer.send(
                    topic="transactions",
                    value=tx.dict(),
                )
                print(
                    f"Sent tx={tx.transaction_id} "
                    f"from={tx.from_account} to={tx.to_account} "
                    f"amount={tx.amount}"
                )

            time.sleep(1 / rate)

    except KeyboardInterrupt:
        print("🛑 Producer stopped.")
    finally:
        producer.flush()
        producer.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--rate", type=int, default=5, help="transactions per second")
    args = parser.parse_args()

    main(rate=args.rate)
