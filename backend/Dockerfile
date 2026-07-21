# ── Backend Dockerfile ─────────────────────────────
# Multi-stage build: development target has hot-reload,
# production target runs gunicorn.

# ── Stage: base ────────────────────────────────────
FROM python:3.11-slim AS base

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

# ── Stage: development ─────────────────────────────
FROM base AS development
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# ── Stage: production ──────────────────────────────
FROM base AS production
RUN pip install --no-cache-dir gunicorn
CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
