"""
SQLAlchemy version of configura_quadro.py

Configures a new quadro (panel) in the system by inserting a record into the T_nodo table
using async SQLAlchemy.
"""
import logging
import asyncio
from typing import Dict, Any, Optional, AsyncGenerator
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# Import models and database session
from models.project import Node
from core.database import get_db as get_async_db


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session"""
    async for session in get_async_db():
        yield session


async def configure_quadro(
    nome_quadro: str, 
    tensione: str, 
    info_ausiliari: str, 
    project_id: int = 1,
    db: Optional[AsyncSession] = None
) -> Dict[str, Any]:
    """
    Configure a new quadro (panel) in the system.
    
    Args:
        nome_quadro: Name of the quadro/panel
        tensione: Voltage of the quadro
        info_ausiliari: Additional information/description
        project_id: Project ID to associate with the quadro (default: 1)
        db: Optional database session (if not provided, a new one will be created)
        
    Returns:
        Dictionary containing the result of the operation
    """
    local_db = False
    if db is None:
        db = await anext(get_db())
        local_db = True
    
    try:
        # Create new node (quadro)
        new_node = Node(
            nome_nodo=nome_quadro,
            tipo_nodo="Quadro",
            descrizione=info_ausiliari,
            id_prg=project_id,
            # Additional fields that might be needed
            tensione=tensione,
            stato=1  # Assuming 1 means active
        )
        
        db.add(new_node)
        await db.commit()
        await db.refresh(new_node)
        
        logger.info("Successfully configured quadro: %s (ID: %s)", nome_quadro, new_node.id_nodo)
        
        return {
            "success": True,
            "message": "Quadro configurato con successo!",
            "node_id": new_node.id_nodo
        }
        
    except SQLAlchemyError as e:
        if local_db:
            await db.rollback()
        logger.error("Error configuring quadro: %s", str(e), exc_info=True)
        return {
            "success": False,
            "message": f"Errore: {str(e)}"
        }
        
    finally:
        if local_db and db:
            await db.close()


# For backward compatibility with existing code
configura_quadro = configure_quadro


async def main():
    """Example usage"""
    # Example: Configure a new quadro
    result = await configure_quadro(
        nome_quadro="Quadro Principale",
        tensione="400V",
        info_ausiliari="Quadro principale di distribuzione"
    )
    print(result["message"])


if __name__ == "__main__":
    asyncio.run(main())
