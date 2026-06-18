FROM python:3.11-slim

# System dependencies for pandas/numpy build
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install numpy && \
    pip install -r requirements.txt

COPY . .
# Apna bot file ka naam yahan daal do
CMD ["python", "main.py"]
