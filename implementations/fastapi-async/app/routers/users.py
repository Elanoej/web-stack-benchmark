from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import User
from app.schemas import HelloResponse, SearchRequest, UserResponse

router = APIRouter(tags=["users"])


@router.get("/users/hello")
async def hello() -> HelloResponse:
    return HelloResponse(message="ok", stack="fastapi-async")


@router.get("/users")
async def list_users(
    page: int = Query(0, ge=0),
    size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> list[UserResponse]:
    stmt = (
        select(User)
        .where(User.active.is_(True))
        .order_by(User.created_at.desc())
        .offset(page * size)
        .limit(size)
    )
    result = await db.execute(stmt)
    rows = result.scalars().all()
    return [UserResponse.model_validate(r) for r in rows]


@router.post("/users/search")
async def search_users(
    body: SearchRequest,
    page: int = Query(0, ge=0),
    size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> list[UserResponse]:
    stmt = select(User).where(User.active.is_(True))

    if body.name:
        stmt = stmt.where(User.name.ilike(f"%{body.name}%"))
    if body.city:
        stmt = stmt.where(User.city.ilike(f"%{body.city}%"))

    stmt = stmt.order_by(User.created_at.desc()).offset(page * size).limit(size)
    result = await db.execute(stmt)
    rows = result.scalars().all()
    return [UserResponse.model_validate(r) for r in rows]
