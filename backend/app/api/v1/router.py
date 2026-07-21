"""
OpsPilot — API v1 Router
===========================
Aggregates all v1 route modules into a single router.
"""

from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.assets import router as assets_router
from app.api.v1.documents import router as documents_router
from app.api.v1.incidents import router as incidents_router
from app.api.v1.maintenance import router as maintenance_router
from app.api.v1.inspections import router as inspections_router
from app.api.v1.copilot import router as copilot_router
from app.api.v1.graph import router as graph_router
from app.api.v1.compliance import router as compliance_router
from app.api.v1.rca import router as rca_router
from app.api.v1.reports import router as reports_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.settings import router as settings_router

api_v1_router = APIRouter()

api_v1_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_v1_router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
api_v1_router.include_router(assets_router, prefix="/assets", tags=["Assets"])
api_v1_router.include_router(documents_router, prefix="/documents", tags=["Documents"])
api_v1_router.include_router(incidents_router, prefix="/incidents", tags=["Incidents"])
api_v1_router.include_router(maintenance_router, prefix="/maintenance", tags=["Maintenance"])
api_v1_router.include_router(inspections_router, prefix="/inspections", tags=["Inspections"])
api_v1_router.include_router(copilot_router, prefix="/copilot", tags=["AI Copilot"])
api_v1_router.include_router(graph_router, prefix="/graph", tags=["Knowledge Graph"])
api_v1_router.include_router(compliance_router, prefix="/compliance", tags=["Compliance"])
api_v1_router.include_router(rca_router, prefix="/rca", tags=["Root Cause Analysis"])
api_v1_router.include_router(reports_router, prefix="/reports", tags=["Reports"])
api_v1_router.include_router(settings_router, prefix="/settings", tags=["Settings"])
