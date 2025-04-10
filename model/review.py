from sqlalchemy import String, DECIMAL, Text, DateTime, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from model.base import Base
import uuid

class Review(Base):
    __tablename__ = "review"
    
    review_uuid: Mapped[str] = mapped_column(
        String(36), primary_key = True, default = lambda: str(uuid.uuid4())
    )
    request_uuid: Mapped[str] = mapped_column(
        String(36)
    )
    user_uuid: Mapped[str] = mapped_column(
        String(36)
    )
    rating: Mapped[float] = mapped_column(
        DECIMAL, nullable = False
    )
    content: Mapped[str] = mapped_column(
        Text, nullable = True
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
            ["user_uuid"],
            ["user.user_uuid"]
        )
    )
    