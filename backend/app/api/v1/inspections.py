"""OpsPilot — Inspection Routes"""

from fastapi import APIRouter, Depends
from app.dependencies import get_current_user_id

router = APIRouter()


@router.get("", summary="List inspections")
async def list_inspections(user_id: str = Depends(get_current_user_id)):
    return {"items": [], "total": 0, "page": 1, "page_size": 20, "total_pages": 0}


@router.post("", summary="Create inspection", status_code=201)
async def create_inspection(user_id: str = Depends(get_current_user_id)):
    return {"message": "Not implemented"}


@router.get("/{inspection_id}", summary="Get inspection detail")
async def get_inspection(inspection_id: str, user_id: str = Depends(get_current_user_id)):
    return {"message": "Not implemented"}
