"""
OpsPilot — Celery Application
================================
Celery worker configuration for asynchronous background tasks.
Used for document processing pipeline and report generation.
"""

import os
from pathlib import Path
from celery import Celery
from dotenv import load_dotenv

# Load .env file from the parent directory of backend (opspilot/.env)
env_path = Path(__file__).resolve().parents[2] / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    load_dotenv()

# Read Redis URL from environment, default for local dev without docker
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "opspilot_worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["worker.tasks.document_tasks", "worker.tasks.report_tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 hour max per task
)
