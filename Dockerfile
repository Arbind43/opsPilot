# ── Stage 1: Builder ──────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app

# Install system dependencies needed for PDF/image processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ── Stage 2: Runtime ──────────────────────────────────────────────────────
FROM python:3.11-slim AS runtime

WORKDIR /app

# Install only runtime system libs
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
# backend/ contains the FastAPI app
COPY backend/ ./backend/
# ai/ contains the pipeline (imported from project root)
COPY ai/ ./ai/

# Create uploads directory
RUN mkdir -p ./backend/storage/uploads

# Set PYTHONPATH so both 'app' and 'ai' packages are resolvable
ENV PYTHONPATH="/app/backend:/app"

WORKDIR /app/backend

EXPOSE 8000

# Use 2 workers — tune based on your cloud plan's RAM
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
