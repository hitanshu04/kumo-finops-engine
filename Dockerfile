# Kumo FinOps Platform - Backend
# Python 3.10
FROM python:3.10-slim


WORKDIR /app

# System tools install kar rahe hain
RUN apt-get update && apt-get install -y gcc libpq-dev

# Python libraries install kar rahe hain
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Code copy kar rahe hain
COPY . .