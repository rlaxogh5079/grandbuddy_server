# models/application.py
from sqlalchemy import String, DateTime, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from model.base_class import Base
from enum import Enum
import uuid

class ApplicationStatus(Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"

class Application(Base):
    __tablename__ = "application"
    application_uuid: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    request_uuid: Mapped[str] = mapped_column(String(36))
    youth_uuid: Mapped[str] = mapped_column(String(36))
    status: Mapped[str] = mapped_column(String(16), default=ApplicationStatus.pending.value)
    created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    __table_args__ = (
        ForeignKeyConstraint(["request_uuid"], ["request.request_uuid"]),
        ForeignKeyConstraint(["youth_uuid"], ["user.user_uuid"]),
    )
    
    def get_attributes(self):
        return {
            "application_uuid": self.application_uuid,
            "request_uuid": self.request_uuid,
            "youth_uuid": self.youth_uuid,
            "status": self.status,
            "created": self.created.isoformat() if self.created else None
        }
