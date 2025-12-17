FROM python:3.10-slim

WORKDIR /app

COPY services/ingestion/requirements.txt .
RUN apt-get update && apt-get install -y gcc
RUN pip install --no-cache-dir -r requirements.txt

# copy the entire services directory to preserve import paths
COPY services/ingestion ./services/ingestion
COPY services/common ./services/common

ENV PYTHONPATH=/app