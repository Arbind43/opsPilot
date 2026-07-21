# ── Worker Dockerfile ─────────────────────────────

FROM python:3.11-slim

WORKDIR /app

# System dependencies for OCR, PDF processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    poppler-utils \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/pyproject.toml ./backend/
RUN pip install --no-cache-dir -e ./backend

# Copy application code
COPY backend/ ./backend/
COPY ai/ ./ai/
COPY worker/ ./worker/

ENV PYTHONPATH=/app/backend:/app

CMD ["celery", "-A", "worker.celery_app", "worker", "--loglevel=info", "--concurrency=4"]
