from sqlalchemy import String, DateTime, Text, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from model.base_class import Base
from enum import Enum
import uuid

class UserRole(Enum):
    senior = 0 # 노인
    youth = 1 # 청년

class User(Base):
    __tablename__ = "user"
    
    user_uuid: Mapped[str] = mapped_column(
        String(36), primary_key = True, default = lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        String(15), unique = True, nullable = False
    )
    password: Mapped[str] = mapped_column(
        String(64), nullable = False
    )
    email: Mapped[str] = mapped_column(
        String(50), unique = True, nullable = False,
    )
    phone: Mapped[str] = mapped_column(
        String(11), nullable = False,
    )
    nickname: Mapped[str] = mapped_column(
        String(15), unique = True, nullable = False
    )
    birthday: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole), nullable = False
    )
    created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default = lambda: datetime.now(timezone.utc)
    )
    address: Mapped[str] = mapped_column(
        Text, nullable = True, default = None
    )
    profile: Mapped[str] = mapped_column(
        Text, nullable = True, default = None
    )
