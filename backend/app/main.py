"""
OpsPilot — FastAPI Application Factory
=======================================
Creates and configures the FastAPI application with all middleware,
routers, and startup/shutdown lifecycle events.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.core.events import on_startup, on_shutdown
from app.core.middleware import register_middleware
from app.api.v1.router import api_v1_router
from app.api.health import health_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan: startup and shutdown hooks."""
    await on_startup()
    yield
    await on_shutdown()


def create_app() -> FastAPI:
    """Build and return the configured FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        description="Industrial Knowledge Intelligence Platform",
        version="0.1.0",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        lifespan=lifespan,
    )

    # ── CORS ─────────────────────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Custom Middleware ────────────────────────
    register_middleware(app)

    # ── Routers ──────────────────────────────────
    app.include_router(health_router)
    app.include_router(api_v1_router, prefix="/api/v1")

    return app


# Application instance used by uvicorn
app = create_app()
