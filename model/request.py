from sqlalchemy import String, DateTime, Text, ForeignKeyConstraint, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from model.base_class import Base
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
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    completed: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default = None, nullable = True
    )
    
    available_start_time: Mapped[datetime] = mapped_column(DateTime(timezone = True), nullable=True)
    available_end_time: Mapped[datetime] = mapped_column(DateTime(timezone = True), nullable=True)

    views: Mapped[int] = mapped_column(default=0)
    applications: Mapped[int] = mapped_column(default=0)
    
    __table_args__ = (
        ForeignKeyConstraint(
            ["senior_uuid"],
            ["user.user_uuid"]
        ),
    )
    
    def get_attributes(self) -> dict:
        return {
            "request_uuid": self.request_uuid,
            "senior_uuid": self.senior_uuid,
            "title": self.title,
            "description": self.description,
            "status": self.status.name,  # Enum은 이름으로 반환
            "created": self.created.isoformat() if self.created else None,
            "completed": self.completed.isoformat() if self.completed else None,
            "available_start_time": self.available_start_time.isformat() if self.available_start_time else None,
            "available_end_time": self.available_end_time.isformat() if self.available_end_time else None,
            "views": self.views,
            "applications": self.applications
        }