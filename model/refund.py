from sqlalchemy import String, Text, DateTime, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from model.base_class import Base
import uuid


class Refund(Base):
    __tablename__ = "refund"
    
    refund_uuid: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    reward_uuid: Mapped[str] = mapped_column(String(36), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=True)
    refunded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        ForeignKeyConstraint(["reward_uuid"], ["reward.reward_uuid"]),
    )