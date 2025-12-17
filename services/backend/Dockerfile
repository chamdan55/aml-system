FROM python:3.10-slim

WORKDIR /app
COPY services/backend/requirements.txt .

RUN apt-get update && apt-get install -y gcc
RUN pip install --no-cache-dir -r requirements.txt

# copy the entire services directory to preserve import paths
COPY services/backend ./services/backend
COPY services/common ./services/common

ENV PYTHONPATH=/app

CMD ["uvicorn", "services.backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]