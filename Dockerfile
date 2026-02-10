# Kumo FinOps Platform - Backend
# Python 3.10
FROM python:3.10-slim

WORKDIR /app

# Install System tools and libraries
RUN apt-get update && apt-get install -y gcc libpq-dev

# Install Python Libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the codebase
COPY . .


# Render expects port 10000.
# 0.0.0.0 allows the app to be accessible from outside the container.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
