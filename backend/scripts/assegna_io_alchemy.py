"""
SQLAlchemy version of assegna_io.py
Automatically assigns I/O to hardware modules using async SQLAlchemy ORM.
"""
import logging
import asyncio
from typing import Dict, List, Optional, Tuple, AsyncGenerator, Any
from sqlalchemy import and_, or_, func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

# Import models and database session
from models.base import Base
from models.hardware import Hardware, IO
from models.project import HardwareNode, Node, Project
from core.database import get_db as get_async_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session"""
    async for session in get_async_db():
        yield session

def get_module_capacity_field(modulo_tipo: str) -> Optional[str]:
    """Map module type to its capacity field"""
    if modulo_tipo == "Input Digitale":
        return "DI"
    elif modulo_tipo == "Output Digitale":
        return "DO"
    elif modulo_tipo == "Input Digitale Fail-Safe":
        return "F-DI"
    elif modulo_tipo == "Output Digitale Fail-Safe":
        return "F-DO"
    elif modulo_tipo in ("Input Analogico Corrente", "Input Analogico Tensione"):
        return "AI"
    elif modulo_tipo in ("Output Analogico Corrente", "Output Analogico Tensione"):
        return "AO"
    return None

async def assign_io_to_module(db: AsyncSession, io_id: int, module_id: int) -> bool:
    """Assign an I/O to a module"""
    try:
        result = await db.execute(select(IO).where(IO.id_io == io_id))
        io = result.scalars().first()
        if not io:
            logger.error(f"I/O with ID {io_id} not found")
            return False
            
        io.id_nodo_hw = module_id
        await db.commit()
        return True
        
    except SQLAlchemyError as e:
        await db.rollback()
        logger.error(f"Error assigning I/O {io_id} to module {module_id}: {e}")
        return False

async def assegna_io_automaticamente(id_prg: int, id_nodo: int, db: Optional[AsyncSession] = None) -> Dict[str, Any]:
    """
    Scans all hardware modules of the node and automatically assigns
    free I/Os (t_io.id_nodo_hw IS NULL) until each module's capacity is filled.
    
    Priority order for module filling is determined by their slot number.
    
    For each module, I/Os of the same type (TipoIO) are taken in groups:
    1. interno_quadro
    2. pulsantiera
    3. bordo_macchina
    4. Any other / NULL
    
    Args:
        id_prg: Project ID
        id_nodo: Node ID
        db: Optional database session (if not provided, a new one will be created)
    """
    local_db = False
    if db is None:
        db = await anext(get_db())
        local_db = True
        
    try:
        # Get all modules for the node, ordered by slot
        result = await db.execute(
            select(HardwareNode)
            .join(Hardware)
            .where(
                HardwareNode.id_prg == id_prg,
                HardwareNode.id_nodo == id_nodo
            )
            .order_by(HardwareNode.slot)
        )
        modules = result.scalars().all()
        
        if not modules:
            return {"success": False, "message": "No hardware modules found for the specified node"}
            
        total_assigned = 0
        
        for module in modules:
            # Get module type and capacity
            result = await db.execute(
                select(Hardware).where(Hardware.id_hw == module.id_hw)
            )
            hw = result.scalars().first()
            
            if not hw:
                logger.warning(f"Hardware not found for module ID {module.id_hw}")
                continue
                
            capacity_field = get_module_capacity_field(hw.tipo_modulo)
            if not capacity_field:
                logger.warning(f"Unknown module type: {hw.tipo_modulo}")
                continue
                
            capacity = getattr(hw, capacity_field, 0)
            if not capacity or capacity <= 0:
                logger.warning(f"Invalid capacity for module {module.id_hw}")
                continue
                
            logger.info(f"Processing module {hw.nome_hw} (Slot {module.slot}) with capacity {capacity}")
            
            # Get count of already assigned I/Os
            result = await db.execute(
                select(func.count(IO.id_io)).where(
                    IO.id_nodo_hw == module.id_nodo_hw
                )
            )
            assigned_count = result.scalar() or 0
            
            remaining_capacity = max(0, capacity - assigned_count)
            
            if remaining_capacity <= 0:
                logger.info(f"  Module at slot {module.slot} is already full")
                continue
                
            logger.info(f"  {remaining_capacity} I/Os can be assigned to this module")
            
            # Get I/Os to assign, ordered by priority
            stmt = (
                select(IO)
                .where(
                    IO.id_prg == id_prg,
                    IO.id_nodo == id_nodo,
                    IO.id_nodo_hw.is_(None),  # Unassigned I/Os
                    IO.TipoIO == hw.tipo_modulo  # Same type as module
                )
                .order_by(
                    func.coalesce(IO.posizione, '').desc(),  # NULLs last
                    IO.id_io  # For consistent ordering
                )
                .limit(remaining_capacity)
            )
            
            result = await db.execute(stmt)
            ios_to_assign = result.scalars().all()
            
            if not ios_to_assign:
                logger.info("  No matching I/Os found to assign")
                continue
                
            # Assign the I/Os
            for io in ios_to_assign:
                success = await assign_io_to_module(db, io.id_io, module.id_nodo_hw)
                if success:
                    total_assigned += 1
                    logger.debug(f"  Assigned I/O {io.id_io} to module {module.id_nodo_hw}")
        
        return {
            "success": True,
            "message": f"Successfully assigned {total_assigned} I/Os",
            "total_assigned": total_assigned
        }
        
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}", exc_info=True)
        if local_db:
            await db.rollback()
        return {
            "success": False,
            "message": f"Database error: {str(e)}"
        }
    finally:
        if local_db and db:
            await db.close()

async def main():
    """Example usage"""
    # Example: Assign I/Os for project 1, node 1
    result = await assegna_io_automaticamente(1, 1)
    print(result["message"])

if __name__ == "__main__":
    asyncio.run(main())
