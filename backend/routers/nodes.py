"""
Node management routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.database import get_db
from core.security import get_current_user
from schemas.project import NodeCreate, NodeResponse
from services.node_service import NodeService

router = APIRouter(prefix="/nodes", tags=["nodes"])
node_service = NodeService()


@router.get("/project/{project_id}", response_model=List[NodeResponse])
async def get_nodes_by_project(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get all nodes for a project"""
    return await node_service.get_nodes_by_project(db, project_id)


@router.post("/", response_model=NodeResponse, status_code=status.HTTP_201_CREATED)
async def create_node(
    node_data: NodeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create a new node"""
    return await node_service.create_node(db, node_data)


@router.post("/plc/auto/{project_id}")
async def create_plc_automatically(
    project_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create PLC automatically"""
    result = await node_service.create_plc_automatically(db, project_id)
    return result
    