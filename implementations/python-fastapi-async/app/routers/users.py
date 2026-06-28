import asyncpg
from fastapi import APIRouter, Depends, Query

from app.database import get_db
from app.schemas import HelloResponse, SearchRequest, UserResponse

router = APIRouter(tags=["users"])


@router.get("/hello")
async def hello() -> HelloResponse:
    return HelloResponse(message="ok", stack="fastapi-async")


@router.get("/users")
async def list_users(
    page: int = Query(0, ge=0),
    size: int = Query(20, ge=1, le=100),
    conn: asyncpg.Connection = Depends(get_db),
) -> list[UserResponse]:
    rows = await conn.fetch(
        "SELECT id, name, email, city, country, age, active, created_at "
        "FROM users WHERE active = TRUE "
        "ORDER BY created_at DESC LIMIT $1 OFFSET $2",
        size, page * size,
    )
    return [UserResponse.model_validate(dict(r)) for r in rows]


@router.post("/users/search")
async def search_users(
    body: SearchRequest,
    page: int = Query(0, ge=0),
    size: int = Query(20, ge=1, le=100),
    conn: asyncpg.Connection = Depends(get_db),
) -> list[UserResponse]:
    clauses = ["active = TRUE"]
    params: list = []
    idx = 1

    if body.name:
        clauses.append(f"name ILIKE ${idx}")
        params.append(f"%{body.name}%")
        idx += 1
    if body.city:
        clauses.append(f"city ILIKE ${idx}")
        params.append(f"%{body.city}%")
        idx += 1

    where = " AND ".join(clauses)
    params.extend([size, page * size])

    rows = await conn.fetch(
        f"SELECT id, name, email, city, country, age, active, created_at "
        f"FROM users WHERE {where} "
        f"ORDER BY created_at DESC LIMIT ${idx} OFFSET ${idx + 1}",
        *params,
    )
    return [UserResponse.model_validate(dict(r)) for r in rows]
