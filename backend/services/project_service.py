"""
Project management service
"""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from models.project import Project
from schemas.project import ProjectCreate, ProjectResponse
from scripts.crea_progetto_alchemy import crea_progetto
import logging

logger = logging.getLogger(__name__)


class ProjectService:
    """Service for handling project-related business logic"""
    
    async def get_projects(self, db: AsyncSession) -> List[ProjectResponse]:
        """Get all projects"""
        try:
            # Use raw SQL for compatibility with existing database
            result = await db.execute(select(Project))
            projects = result.scalars().all()
            return [ProjectResponse.from_orm(project) for project in projects]
        except Exception as e:
            logger.error(f"Error getting projects: {e}")
            raise
    
    async def get_project_by_id(self, db: AsyncSession, project_id: int) -> Optional[ProjectResponse]:
        """Get project by ID"""
        try:
            result = await db.execute(
                select(Project).where(Project.id_prg == project_id)
            )
            project = result.scalar_one_or_none()
            if project:
                return ProjectResponse.from_orm(project)
            return None
        except Exception as e:
            logger.error(f"Error getting project {project_id}: {e}")
            raise
    
    async def create_project(self, db: AsyncSession, project_data: ProjectCreate, username: str) -> ProjectResponse:
        """Create a new project"""
        try:
            # Use the existing crea_progetto function for compatibility
            project_id = await self._create_project_legacy(
                project_data.nome_progetto, 
                project_data.descrizione,
                username
            )
            
            # Get the created project
            created_project = await self.get_project_by_id(db, project_id)
            if not created_project:
                raise Exception("Failed to retrieve created project")
            
            return created_project
        except Exception as e:
            logger.error(f"Error creating project: {e}")
            raise
    
    async def delete_project(self, db: AsyncSession, project_id: int) -> bool:
        """Delete a project"""
        try:
            # Check if project exists
            project = await self.get_project_by_id(db, project_id)
            if not project:
                return False
            
            # Delete project (cascading deletes will handle related data)
            await db.execute(delete(Project).where(Project.id_prg == project_id))
            await db.commit()
            
            return True
        except Exception as e:
            logger.error(f"Error deleting project {project_id}: {e}")
            await db.rollback()
            raise
    
    async def _create_project_legacy(self, nome: str, descrizione: str, username: str) -> int:
        """Create project using legacy function"""
        try:
            from datetime import datetime
            # Use the existing crea_progetto function with current datetime
            current_time = datetime.now()
            result = await crea_progetto(nome, descrizione, current_time)
            
            # Get the project ID by querying the latest project with this name
            from sqlalchemy import select
            from models.project import Project
            from core.database import get_db
            
            async for db in get_db():
                result = await db.execute(
                    select(Project)
                    .where(Project.nome_progetto == nome)
                    .order_by(Project.id_prg.desc())
                )
                project = result.scalars().first()
                if project:
                    # The username is not used in the legacy function, but we can log it
                    logger.info(f"Project created by user: {username}")
                    return int(project.id_prg)
                
            raise Exception("Failed to retrieve created project ID")
            
        except Exception as e:
            logger.error(f"Error in legacy project creation: {e}")
            raise
        