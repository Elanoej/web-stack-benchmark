from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.database import init_db, close_db
from app.routers.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()


app = FastAPI(
    lifespan=lifespan,
    title="fastapi-async",
    default_response_class=ORJSONResponse,
)
app.include_router(users_router)
