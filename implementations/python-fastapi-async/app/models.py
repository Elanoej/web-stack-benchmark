import uuid
from datetime import datetime

from sqlalchemy import Boolean, Integer, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150))
    city: Mapped[str] = mapped_column(String(100))
    country: Mapped[str] = mapped_column(String(100))
    age: Mapped[int] = mapped_column(Integer)
    active: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
