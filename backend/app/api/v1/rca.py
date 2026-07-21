"""OpsPilot — Root Cause Analysis Routes"""

from fastapi import APIRouter, Depends
from app.dependencies import get_current_user_id

router = APIRouter()


@router.post("/analyze", summary="Run RCA")
async def run_rca(user_id: str = Depends(get_current_user_id)):
    return {"message": "Not implemented"}


@router.get("", summary="List RCA analyses")
async def list_rca(user_id: str = Depends(get_current_user_id)):
    return {"items": []}


@router.get("/{rca_id}", summary="Get RCA result")
async def get_rca(rca_id: str, user_id: str = Depends(get_current_user_id)):
    return {"message": "Not implemented"}
