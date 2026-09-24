FROM python:3.11-slim as builder

WORKDIR /app

COPY requirements.txt requirements-detailed.txt ./

RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r requirements-detailed.txt

FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

COPY . .

CMD ["python", "scripts/pipeline.py", "--input_folder", "./data/data_test", "--output_folder", "./output", "--model_folder", "./data/models", "--output_format", "excel"]