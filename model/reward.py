from sqlalchemy import String, DateTime, Text, Integer, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from model.base_class import Base
import uuid

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