from sqlalchemy import String, DateTime, Text, Integer, ForeignKeyConstraint, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from model.base_class import Base
from enum import Enum
import uuid

class RewardStatus(Enum):
    awarded = 0 # 활성화
    canceld = 1 # 취소됨
    refunded = 2 # 환불됨


# Reward 모델에 필드 추가

class Reward(Base):
    __tablename__ = "reward"
    
    reward_uuid: Mapped[str] = mapped_column(
        String(36), primary_key = True, default = lambda: str(uuid.uuid4())
    )
    youth_uuid: Mapped[str] = mapped_column(
        String(36), nullable = False
    )
    points: Mapped[int] = mapped_column(
        Integer, nullable = False
    )
    status: Mapped[RewardStatus] = mapped_column(
       SQLEnum(RewardStatus), default=RewardStatus.awarded, nullable=False
    )
    description: Mapped[str] = mapped_column(
        Text, nullable = True
    )
    created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    
    __table_args__ = (
        ForeignKeyConstraint(
            ["youth_uuid"],
            ["user.user_uuid"]
        ),
    )