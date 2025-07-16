"""
SQLAlchemy version of crea_progetto.py

Creates a new project in the database using async SQLAlchemy.
"""
import logging
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional, AsyncGenerator
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# Import models and database session
from models.project import Project
from core.database import get_db as get_async_db


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session"""
    async for session in get_async_db():
        yield session


async def create_project(
    project_name: str,
    description: str,
    creation_date: Optional[datetime] = None,
    db: Optional[AsyncSession] = None
) -> Dict[str, Any]:
    """
    Create a new project in the database.
    
    Args:
        project_name: Name of the project
        description: Project description
        creation_date: Optional creation date (defaults to current datetime)
        db: Optional database session (if not provided, a new one will be created)
        
    Returns:
        Dictionary containing the result of the operation
    """
    local_db = False
    if db is None:
        db = await anext(get_db())
        local_db = True
    
    try:
        # Set default creation date if not provided
        if creation_date is None:
            creation_date = datetime.now()
        
        # Create new project
        new_project = Project(
            nome_progetto=project_name,
            descrizione=description,
            data_creazione=creation_date
        )
        
        db.add(new_project)
        await db.commit()
        await db.refresh(new_project)
        
        logger.info(
            f"Created new project: {new_project.nome_progetto} "
            f"(ID: {new_project.id_prg})"
        )
        
        return {
            "success": True,
            "message": "Project created successfully!",
            "project_id": new_project.id_prg,
            "project_name": new_project.nome_progetto,
            "creation_date": new_project.data_creazione.isoformat()
        }
        
    except SQLAlchemyError as e:
        if local_db:
            await db.rollback()
        logger.error(f"Error creating project: {e}", exc_info=True)
        return {
            "success": False,
            "message": f"Error creating project: {str(e)}"
        }
    finally:
        if local_db and db:
            await db.close()


# For backward compatibility
async def crea_progetto(
    nome_progetto: str,
    descrizione_progetto: str,
    data_creazione: Optional[datetime] = None
) -> str:
    """
    Legacy function for backward compatibility.
    
    Args:
        nome_progetto: Project name
        descrizione_progetto: Project description
        data_creazione: Optional creation date
        
    Returns:
        Success or error message
    """
    result = await create_project(nome_progetto, descrizione_progetto, data_creazione)
    return result["message"] if result["success"] else f"Error: {result['message']}"


async def main():
    # Example usage
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python crea_progetto_alchemy.py <project_name> <description> [creation_date]")
        sys.exit(1)
    
    project_name = sys.argv[1]
    description = sys.argv[2]
    creation_date = sys.argv[3] if len(sys.argv) > 3 else None
    
    if creation_date:
        try:
            creation_date = datetime.fromisoformat(creation_date)
        except ValueError:
            print(f"Error: Invalid date format. Please use ISO format (YYYY-MM-DD[THH:MM:SS])")
            sys.exit(1)
    
    result = await create_project(project_name, description, creation_date)
    print(result["message"])

if __name__ == "__main__":
    asyncio.run(main())
