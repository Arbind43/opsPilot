# ── OpsPilot Backend — Dockerfile ─────────────────────────────────────────
# Build context is the repo ROOT (not backend/).
# Render: set "Root Directory" to "." and "Dockerfile Path" to "backend/Dockerfile"
#
# ── Stage 1: Builder ──────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app

# System dependencies needed for PDF/image processing and OCR
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1 \
    libglib2.0-0 \
    tesseract-ocr \
    poppler-utils \
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
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
# backend/ contains the FastAPI app; ai/ contains the pipeline
COPY backend/ ./backend/
COPY ai/ ./ai/

# Create storage directory for uploads
RUN mkdir -p ./backend/storage/uploads

# Set PYTHONPATH so both 'app' (in backend/) and 'ai' (in root) packages resolve
ENV PYTHONPATH="/app/backend:/app"

WORKDIR /app/backend

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
