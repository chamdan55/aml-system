# AML Investigation System
A full-stack anti-money laundering (AML) investigation platform with streaming ingestion, graph analytics, rule engine, ML scoring, and an investigator UI. Built for showcasing data engineering, backend, frontend, ML, and observability skills.

## Features
- Streaming transaction ingestion (Kafka)
- Raw landing to object storage (MinIO) and Postgres
- Graph construction (Neo4j) and graph-based detections
- Rule engine + ML scoring for suspiciousness
- Investigator dashboard with interactive graph explorer
- MLOps basics: MLflow model registry, Airflow orchestrations
- Observability with Prometheus/Grafana and logs

## Techstack
Python, FastAPI, React + TypeScript, Kafka, Neo4j, Postgres, MinIO, Airflow, MLflow, Docker

## Quickstart (local)
Prereqs: Docker & Docker Compose

1. Clone repo
2. `docker compose up --build`
3. Run the data producer: `python services/ingestion/producer.py --rate 10`
4. Open UI: `http://localhost:3000`
5. Open API docs: `http://localhost:8000/docs`

## Repo layout
(brief description + pointers to key folders)

## How to demo
- Start the stack
- Start producer to send synthetic transactions
- Open UI and inspect generated alerts
- Click into a case, view graph, add investigator notes

## Design decisions
- Why Neo4j for graph storage
- Rule engine as microservice vs embedded
- Model choices & explainability

## Next steps / improvements
- Deploy to Kubernetes
- Add federated learning across banks
- Integrate real KYC document parsing
