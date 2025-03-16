FROM python:3.10-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python -m ensurepip --default-pip && \
    pip install --no-cache-dir --upgrade pip setuptools wheel

RUN pip install --no-cache-dir spacy==3.7.0 && \
    python -m spacy download es_core_news_md

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.routers.hyperstition:router", "--host", "0.0.0.0", "--port", "8000"]