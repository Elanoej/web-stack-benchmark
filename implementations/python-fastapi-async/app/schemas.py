import uuid
from datetime import datetime

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    city: str
    country: str
    age: int
    active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class SearchRequest(BaseModel):
    name: str | None = None
    city: str | None = None


class HelloResponse(BaseModel):
    message: str
    stack: str
