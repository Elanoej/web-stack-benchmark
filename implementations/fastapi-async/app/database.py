from collections.abc import AsyncGenerator

from pydantic_settings import BaseSettings
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://bench:bench123@localhost:5432/benchmark"


settings = Settings()

engine = create_async_engine(
    settings.database_url,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    pass


async def close_db():
    await engine.dispose()


async def get_db() -> AsyncGenerator[AsyncSession]:
    async with async_session() as session:
        yield session
