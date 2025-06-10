from sqlalchemy import String, DateTime, ForeignKeyConstraint, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from model.base_class import Base
from typing import Dict, Any
from enum import Enum
import uuid

class MatchStatus(Enum):
    active = 0       # 매칭 진행 중 (수락됨)
    declined = 1     # 거절됨/취소
    completed = 2    # 완료됨

class Match(Base):
    __tablename__ = "match"
    
    match_uuid: Mapped[str] = mapped_column(
        String(36), primary_key = True, default = lambda: str(uuid.uuid4())
    )
    request_uuid: Mapped[str] = mapped_column(
        String(36)
    )
    youth_uuid: Mapped[str] = mapped_column(
        String(36)
    )
    status: Mapped[MatchStatus] = mapped_column(
        SQLEnum(MatchStatus), nullable = False
    )
    created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    
    
    __table_args__ = (
        ForeignKeyConstraint(
            ["request_uuid"],
            ["request.request_uuid"]
        ),
        ForeignKeyConstraint(
            ["youth_uuid"],
            ["user.user_uuid"]
        )
    )
    
    def get_attributes(self) -> Dict[str, Any]:
        return {
            "match_uuid": self.match_uuid,
            "request_uuid": self.request_uuid,
            "youth_uuid": self.youth_uuid,
            "status": self.status.name,
            "created": self.created.isoformat() if self.created else None
        }