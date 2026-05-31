from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import engine
from app.routers.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan, title="fastapi-async")
app.include_router(users_router)
