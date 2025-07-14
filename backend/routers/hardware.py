"""
Hardware management routes
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from core.database import get_db
from core.security import get_current_user
from schemas.hardware import HardwareResponse, HardwareNodeCreate, HardwareNodeResponse
from services.hardware_service import HardwareService

router = APIRouter(prefix="/hardware", tags=["hardware"])
hardware_service = HardwareService()


@router.get("/catalog", response_model=List[HardwareResponse])
async def get_hardware_catalog(
    tipo: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get hardware catalog with optional filtering by type"""
    return await hardware_service.get_hardware_catalog(db, tipo)


@router.get("/node/{node_id}", response_model=List[HardwareNodeResponse])
async def get_node_hardware(
    node_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get hardware assigned to a node"""
    return await hardware_service.get_node_hardware(db, node_id)


@router.post("/node", response_model=HardwareNodeResponse, status_code=status.HTTP_201_CREATED)
async def add_hardware_to_node(
    hardware_data: HardwareNodeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Add hardware to a node"""
    return await hardware_service.add_hardware_to_node(db, hardware_data)


@router.delete("/node/{hardware_node_id}")
async def remove_hardware_from_node(
    hardware_node_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Remove hardware from a node"""
    success = await hardware_service.remove_hardware_from_node(db, hardware_node_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hardware node not found"
        )
    return {"message": "Hardware removed from node successfully"}