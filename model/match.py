from sqlalchemy import String, DateTime, ForeignKeyConstraint, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from model.base import Base
from enum import Enum
import uuid

class MatchStatus(Enum):
    accepted = 0 # 수락 됨
    declined = 1 # 거절 됨
    in_progress = 2 # 진행 중
    completed = 3 # 완료 됨

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
        DateTime, default = lambda: datetime.now()
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