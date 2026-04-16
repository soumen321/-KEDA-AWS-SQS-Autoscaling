# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY src/consumer.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "consumer.py"]
