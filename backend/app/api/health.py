"""
OpsPilot — Health Check Routes
=================================
Basic health and readiness endpoints (no auth required).
"""

from fastapi import APIRouter

health_router = APIRouter(tags=["Health"])


@health_router.get("/health", summary="Basic health check")
async def health():
    """Returns 200 if the application is running."""
    return {"status": "ok", "service": "opspilot"}


@health_router.get("/health/ready", summary="Readiness check")
async def readiness():
    """Checks that all dependent services are reachable."""
    checks: dict = {}

    # PostgreSQL check
    try:
        from app.db.session import engine
        async with engine.connect() as conn:
            await conn.execute(
                __import__("sqlalchemy").text("SELECT 1")
            )
        checks["postgres"] = "ok"
    except Exception as e:
        checks["postgres"] = f"error: {str(e)}"

    # Neo4j check
    try:
        from app.db.neo4j_client import neo4j_client
        neo4j_client.verify_connectivity()
        checks["neo4j"] = "ok"
    except Exception as e:
        checks["neo4j"] = f"error: {str(e)}"

    # Pinecone check
    try:
        from app.db.pinecone_client import pinecone_client
        pinecone_client.heartbeat()
        checks["pinecone"] = "ok"
    except Exception as e:
        checks["pinecone"] = f"error: {str(e)}"

    all_ok = all(v == "ok" for v in checks.values())
    return {"status": "ready" if all_ok else "degraded", "checks": checks}
