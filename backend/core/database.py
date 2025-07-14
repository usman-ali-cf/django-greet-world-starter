"""
Database configuration and session management with async SQLAlchemy 2.x
"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.pool import StaticPool
from core.config import settings
import logging

logger = logging.getLogger(__name__)

# Convert sqlite URL to async version
async_database_url = settings.database_url.replace("sqlite:///", "sqlite+aiosqlite:///")

# Create async engine
engine = create_async_engine(
    async_database_url,
    poolclass=StaticPool,
    connect_args={"check_same_thread": False},
    echo=settings.debug,
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
    Initialize database tables
    """
    try:
        # Import all models to ensure they are registered
        from models import *
        
        async with engine.begin() as conn:
            # For now, we won't create tables as we're working with existing SQLite database
            # await conn.run_sync(Base.metadata.create_all)
            pass
        
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise