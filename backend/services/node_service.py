"""
Node management service
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from models.project import Node
from schemas.project import NodeCreate, NodeResponse
from scripts.crea_nodo_alchemy import crea_nodo_plc_automatico
import logging

logger = logging.getLogger(__name__)


class NodeService:
    """Service for handling node-related business logic"""
    
    async def get_nodes_by_project(self, db: AsyncSession, project_id: int) -> List[NodeResponse]:
        """Get all nodes for a project"""
        try:
            result = await db.execute(
                select(Node).where(Node.id_prg == project_id).order_by(Node.nome_nodo)
            )
            nodes = result.scalars().all()
            return [NodeResponse.from_orm(node) for node in nodes]
        except Exception as e:
            logger.error(f"Error getting nodes for project {project_id}: {e}")
            raise
    
    async def create_node(self, db: AsyncSession, node_data: NodeCreate) -> NodeResponse:
        """Create a new node"""
        try:
            node = Node(
                nome_nodo=node_data.nome_nodo,
                tipo_nodo=node_data.tipo_nodo or 'PLC',
                descrizione=node_data.descrizione,
                id_prg=node_data.id_prg,
                id_quadro=node_data.id_quadro
            )
            db.add(node)
            await db.commit()
            await db.refresh(node)
            return NodeResponse.from_orm(node)
        except Exception as e:
            logger.error(f"Error creating node: {e}")
            await db.rollback()
            raise
    
    async def create_plc_automatically(self, db: AsyncSession, project_id: int) -> dict:
        """Create PLC automatically using legacy function"""
        try:
            # Use existing function but adapt for async context
            result = await crea_nodo_plc_automatico(project_id, db)
            return result
        except Exception as e:
            logger.error(f"Error creating automatic PLC: {e}")
            raise