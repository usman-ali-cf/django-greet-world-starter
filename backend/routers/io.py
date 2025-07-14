"""
I/O management routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from core.database import get_db
from core.security import get_current_user
from schemas.io import IOResponse, IOAssignRequest, IORemoveRequest
from services.io_service import IOService

router = APIRouter(prefix="/io", tags=["io"])
io_service = IOService()


@router.get("/unassigned", response_model=List[IOResponse])
async def get_unassigned_io(
    project_id: int = Query(...),
    tipo: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get unassigned I/O for a project"""
    return await io_service.get_unassigned_io(db, project_id, tipo)


@router.get("/assigned", response_model=List[IOResponse])
async def get_assigned_io(
    module_id: int = Query(...),
    node_id: int = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get I/O assigned to a specific module"""
    return await io_service.get_assigned_io(db, module_id, node_id)


@router.post("/assign")
async def assign_io(
    assign_data: IOAssignRequest,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Assign I/O to a module"""
    result = await io_service.assign_io(db, assign_data)
    return result


@router.delete("/assign/{io_id}")
async def remove_io_assignment(
    io_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Remove I/O assignment"""
    result = await io_service.remove_io_assignment(db, io_id)
    return result


@router.post("/assign/auto")
async def assign_io_automatically(
    node_id: int = Query(...),
    project_id: int = Query(...),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Assign I/O automatically"""
    result = await io_service.assign_io_automatically(db, node_id, project_id)
    return result