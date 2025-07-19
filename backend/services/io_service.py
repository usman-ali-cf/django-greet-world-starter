"""
I/O management service
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from models.hardware import IO
from schemas.io import IOResponse, IOAssignRequest, IORemoveRequest
from scripts.assegna_io_alchemy import assegna_io_automaticamente
import logging

logger = logging.getLogger(__name__)


class IOService:
    """Service for handling I/O-related business logic"""
    
    async def get_unassigned_io(self, db: AsyncSession, project_id: int, tipo: Optional[str] = None) -> List[IOResponse]:
        """Get unassigned I/O for a project"""
        try:
            query = select(IO).where(IO.id_prg == project_id, IO.id_modulo.is_(None))
            
            if tipo:
                query = query.where(IO.tipo == tipo)
                
            query = query.order_by(IO.tipo, IO.codice)
            
            result = await db.execute(query)
            ios = result.scalars().all()
            
            return [IOResponse.model_validate(io) for io in ios]
        except Exception as e:
            logger.error(f"Error getting unassigned I/O: {e}")
            raise
    
    async def get_assigned_io(self, db: AsyncSession, module_id: int, node_id: int) -> List[IOResponse]:
        """Get I/O assigned to a specific module"""
        try:
            query = select(IO).where(IO.id_modulo == module_id).order_by(IO.tipo, IO.codice)
            result = await db.execute(query)
            ios = result.scalars().all()
            
            return [IOResponse.model_validate(io) for io in ios]
        except Exception as e:
            logger.error(f"Error getting assigned I/O: {e}")
            raise
    
    async def assign_io(self, db: AsyncSession, assign_data: IOAssignRequest) -> dict:
        """Assign I/O to a module"""
        try:
            # Check if I/O is already assigned
            result = await db.execute(
                select(IO.id_modulo).where(IO.id_io == assign_data.id_io)
            )
            current_assignment = result.scalar()
            
            if current_assignment:
                return {"error": "I/O già assegnato ad un altro modulo"}
            
            # Assign I/O to module
            await db.execute(
                update(IO)
                .where(IO.id_io == assign_data.id_io)
                .values(
                    id_modulo=assign_data.id_modulo,
                    indirizzo=assign_data.indirizzo,
                    note=assign_data.note
                )
            )
            await db.commit()
            
            return {"success": True, "message": "I/O assegnato con successo"}
        except Exception as e:
            logger.error(f"Error assigning I/O: {e}")
            await db.rollback()
            raise
    
    async def remove_io_assignment(self, db: AsyncSession, io_id: int) -> dict:
        """Remove I/O assignment"""
        try:
            await db.execute(
                update(IO)
                .where(IO.id_io == io_id)
                .values(id_modulo=None, indirizzo=None)
            )
            await db.commit()
            
            return {"success": True, "message": "Assegnazione I/O rimossa con successo"}
        except Exception as e:
            logger.error(f"Error removing I/O assignment: {e}")
            await db.rollback()
            raise
    
    async def assign_io_automatically(self, db: AsyncSession, node_id: int, project_id: int) -> dict:
        """Assign I/O automatically using legacy function"""
        try:
            # Use existing function
            result = assegna_io_automaticamente(project_id, node_id)
            return result
        except Exception as e:
            logger.error(f"Error in automatic I/O assignment: {e}")
            raise