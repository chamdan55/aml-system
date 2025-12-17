#!/bin/bash
set -euo pipefail

# Bootstrap server can be overridden via BOOTSTRAP_SERVER env var.
# Default aligns with docker-compose internal listener for the broker.
BOOTSTRAP_SERVER="${BOOTSTRAP_SERVER:-kafka:29092}"

# Comma-separated list of topic specs in the form name:partitions:replication
# e.g. "transactions:3:1,alerts:1:1". Defaults to a single transactions topic.
KAFKA_TOPICS="${KAFKA_TOPICS:-transactions:3:1}"

echo "Waiting for Kafka at ${BOOTSTRAP_SERVER} ..."
for i in {1..30}; do
  if kafka-topics --bootstrap-server "${BOOTSTRAP_SERVER}" --list >/dev/null 2>&1; then
    echo "Kafka is reachable."
    break
  fi
  sleep 2
  echo -n "."
  if [ "$i" -eq 30 ]; then
    echo "\nKafka did not become ready in time." >&2
    exit 1
  fi
done

IFS=',' read -ra TOPIC_SPECS <<< "${KAFKA_TOPICS}"
for spec in "${TOPIC_SPECS[@]}"; do
  IFS=':' read -r name partitions replication <<< "${spec}"
  partitions="${partitions:-1}"
  replication="${replication:-1}"
  if [ "$replication" -gt 1 ]; then
  echo "Warning: replication-factor=${replication} on single-broker cluster"
  fi
  if [ -z "${name}" ]; then
    continue
  fi
  echo "Ensuring topic '${name}' exists (partitions=${partitions}, rf=${replication}) ..."
  kafka-topics \
    --bootstrap-server "${BOOTSTRAP_SERVER}" \
    --create \
    --if-not-exists \
    --topic "${name}" \
    --partitions "${partitions}" \
    --replication-factor "${replication}"
done

echo "Kafka topics ready"