"""
I/O management service
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from schemas.io import IOResponse, IOAssignRequest, IORemoveRequest
from scripts.assegna_io_alchemy import assegna_io_automaticamente
import logging

logger = logging.getLogger(__name__)


class IOService:
    """Service for handling I/O-related business logic"""
    
    async def get_unassigned_io(self, db: AsyncSession, project_id: int, tipo: Optional[str] = None) -> List[IOResponse]:
        """Get unassigned I/O for a project"""
        try:
            query = """
                SELECT id_io, codice, descrizione, tipo, id_modulo, indirizzo, note, id_prg
                FROM t_io
                WHERE id_prg = :project_id AND id_modulo IS NULL
            """
            params = {"project_id": project_id}
            
            if tipo:
                query += " AND tipo = :tipo"
                params["tipo"] = tipo
                
            query += " ORDER BY tipo, codice"
            
            result = await db.execute(text(query), params)
            rows = result.fetchall()
            
            ios = []
            for row in rows:
                row_dict = dict(row._mapping)
                ios.append(IOResponse(**row_dict))
            
            return ios
        except Exception as e:
            logger.error(f"Error getting unassigned I/O: {e}")
            raise
    
    async def get_assigned_io(self, db: AsyncSession, module_id: int, node_id: int) -> List[IOResponse]:
        """Get I/O assigned to a specific module"""
        try:
            result = await db.execute(
                text("""
                    SELECT id_io, codice, descrizione, tipo, id_modulo, indirizzo, note, id_prg
                    FROM t_io
                    WHERE id_modulo = :module_id
                    ORDER BY tipo, codice
                """),
                {"module_id": module_id}
            )
            rows = result.fetchall()
            
            ios = []
            for row in rows:
                row_dict = dict(row._mapping)
                ios.append(IOResponse(**row_dict))
            
            return ios
        except Exception as e:
            logger.error(f"Error getting assigned I/O: {e}")
            raise
    
    async def assign_io(self, db: AsyncSession, assign_data: IOAssignRequest) -> dict:
        """Assign I/O to a module"""
        try:
            # Check if I/O is already assigned
            result = await db.execute(
                text("SELECT id_modulo FROM t_io WHERE id_io = :io_id"),
                {"io_id": assign_data.id_io}
            )
            current_assignment = result.scalar()
            
            if current_assignment:
                return {"error": "I/O già assegnato ad un altro modulo"}
            
            # Assign I/O to module
            await db.execute(
                text("""
                    UPDATE t_io 
                    SET id_modulo = :module_id, indirizzo = :indirizzo, note = :note
                    WHERE id_io = :io_id
                """),
                {
                    "module_id": assign_data.id_modulo,
                    "indirizzo": assign_data.indirizzo,
                    "note": assign_data.note,
                    "io_id": assign_data.id_io
                }
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
                text("""
                    UPDATE t_io 
                    SET id_modulo = NULL, indirizzo = NULL
                    WHERE id_io = :io_id
                """),
                {"io_id": io_id}
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