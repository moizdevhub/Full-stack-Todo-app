from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
import os
from typing import AsyncGenerator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost:5432/todo_app")

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True if os.getenv("ENVIRONMENT") == "development" else False,
    future=True,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,  # Test connections before using them to avoid stale connections
    pool_recycle=3600,   # Recycle connections after 1 hour to prevent timeout issues
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting async database sessions."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """Initialize database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
