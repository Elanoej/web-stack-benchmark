import os
from collections.abc import AsyncGenerator

import asyncpg
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://bench:bench123@localhost:5432/benchmark"


settings = Settings()

_workers = int(os.getenv("WORKERS", "1"))
pool_size = int(os.getenv("POOL_SIZE", str(max(2, 30 // _workers))))

pool: asyncpg.Pool | None = None


async def init_db():
    global pool
    dsn = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")
    pool = await asyncpg.create_pool(
        dsn=dsn,
        min_size=pool_size,
        max_size=pool_size,
    )


async def close_db():
    if pool is not None:
        await pool.close()


async def get_db() -> AsyncGenerator[asyncpg.Connection]:
    if pool is None:
        raise RuntimeError("pool not initialized")
    async with pool.acquire() as conn:
        yield conn
