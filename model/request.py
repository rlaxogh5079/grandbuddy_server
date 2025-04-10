from sqlalchemy import String, DateTime, Text, ForeignKeyConstraint, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from model.base import Base
from enum import Enum
import uuid

class RequestStatus(Enum):
    pending = 0 # 대기 중
    accepted = 1 # 처리 됨
    completed = 2 # 완료 됨
    canceld = 3 # 취소 됨

class Request(Base):
    __tablename__ = "request"
    
    request_uuid: Mapped[str] = mapped_column(
        String(36), primary_key = True, default = lambda: str(uuid.uuid4())
    )
    senior_uuid: Mapped[str] = mapped_column(
        String(36)
    )
    title: Mapped[str] = mapped_column(
        Text, nullable = False
    )
    description: Mapped[str] = mapped_column(
        Text, nullable = True, default = None
    )
    status: Mapped[RequestStatus] = mapped_column(
        SQLEnum(RequestStatus), default = RequestStatus.pending
    )
    created: Mapped[datetime] = mapped_column(
        DateTime, default = lambda: datetime.now()
    )
    completed: Mapped[datetime] = mapped_column(
        DateTime, default = None
    )
    
    __table_args__ = (
        ForeignKeyConstraint(
            ["senior_uuid"],
            ["user.user_uuid"]
        ),
    )