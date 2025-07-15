"""
Database configuration and session management with async SQLAlchemy 2.x for PostgreSQL
"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import NullPool
from core.config import settings
import logging

logger = logging.getLogger(__name__)

# Use the database URL directly from settings (already in asyncpg format)
async_database_url = settings.database_url

# Create async engine for PostgreSQL
engine = create_async_engine(
    async_database_url,
    poolclass=NullPool,  # Using NullPool for better async performance with PostgreSQL
    echo=settings.debug,
    future=True
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
)

# Base class for models
Base = declarative_base()


async def get_db() -> AsyncSession:
    """
    Dependency function to get database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_database():
    """
    Initialize database tables for PostgreSQL
    """
    try:
        # Import all models to ensure they are registered
        from models import Base, Project, Node, HardwareNode, Hardware, IO, User
        
        async with engine.begin() as conn:
            # Create all tables
            await conn.run_sync(Base.metadata.create_all)
        
        logger.info("PostgreSQL database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise