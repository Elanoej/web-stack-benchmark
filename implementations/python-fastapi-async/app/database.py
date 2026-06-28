import os
from collections.abc import AsyncGenerator

from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://bench:bench123@localhost:5432/benchmark"


settings = Settings()

_workers = int(os.getenv("WORKERS", "1"))
pool_size = int(os.getenv("POOL_SIZE", str(max(2, 30 // _workers))))

engine = create_async_engine(
    settings.database_url,
    pool_size=pool_size,
    max_overflow=0,
    pool_pre_ping=False,
)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    pass


async def close_db():
    await engine.dispose()


async def get_db() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        yield session
