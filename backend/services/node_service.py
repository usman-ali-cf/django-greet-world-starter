"""
Node management service
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, text
from models.project import Node
from schemas.project import NodeCreate, NodeResponse
from scripts.crea_nodo import crea_nodo_plc_automatico
import logging

logger = logging.getLogger(__name__)


class NodeService:
    """Service for handling node-related business logic"""
    
    async def get_nodes_by_project(self, db: AsyncSession, project_id: int) -> List[NodeResponse]:
        """Get all nodes for a project"""
        try:
            # Use raw SQL for compatibility
            result = await db.execute(
                text("SELECT * FROM t_nodo WHERE id_prg = :project_id ORDER BY nome_nodo"),
                {"project_id": project_id}
            )
            rows = result.fetchall()
            
            nodes = []
            for row in rows:
                node_dict = dict(row._mapping)
                nodes.append(NodeResponse(**node_dict))
            
            return nodes
        except Exception as e:
            logger.error(f"Error getting nodes for project {project_id}: {e}")
            raise
    
    async def create_node(self, db: AsyncSession, node_data: NodeCreate) -> NodeResponse:
        """Create a new node"""
        try:
            # Use raw SQL for compatibility
            result = await db.execute(
                text("""
                    INSERT INTO t_nodo (nome_nodo, tipo_nodo, descrizione, id_prg, id_quadro)
                    VALUES (:nome_nodo, :tipo_nodo, :descrizione, :id_prg, :id_quadro)
                    RETURNING id_nodo
                """),
                {
                    "nome_nodo": node_data.nome_nodo,
                    "tipo_nodo": node_data.tipo_nodo or 'PLC',
                    "descrizione": node_data.descrizione,
                    "id_prg": node_data.id_prg,
                    "id_quadro": node_data.id_quadro
                }
            )
            
            # For SQLite, we need to handle this differently
            await db.execute(
                text("""
                    INSERT INTO t_nodo (nome_nodo, tipo_nodo, descrizione, id_prg, id_quadro)
                    VALUES (:nome_nodo, :tipo_nodo, :descrizione, :id_prg, :id_quadro)
                """),
                {
                    "nome_nodo": node_data.nome_nodo,
                    "tipo_nodo": node_data.tipo_nodo or 'PLC',
                    "descrizione": node_data.descrizione,
                    "id_prg": node_data.id_prg,
                    "id_quadro": node_data.id_quadro
                }
            )
            await db.commit()
            
            # Get the created node
            result = await db.execute(
                text("SELECT * FROM t_nodo WHERE nome_nodo = :nome_nodo AND id_prg = :id_prg ORDER BY id_nodo DESC LIMIT 1"),
                {"nome_nodo": node_data.nome_nodo, "id_prg": node_data.id_prg}
            )
            row = result.fetchone()
            
            if row:
                node_dict = dict(row._mapping)
                return NodeResponse(**node_dict)
            else:
                raise Exception("Failed to retrieve created node")
                
        except Exception as e:
            logger.error(f"Error creating node: {e}")
            await db.rollback()
            raise
    
    async def create_plc_automatically(self, db: AsyncSession, project_id: int) -> dict:
        """Create PLC automatically using legacy function"""
        try:
            # Use existing function but adapt for async context
            result = crea_nodo_plc_automatico(project_id)
            return result
        except Exception as e:
            logger.error(f"Error creating automatic PLC: {e}")
            raise