from sqlalchemy import String, DateTime, Text, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from model.base import Base
import uuid

class Message(Base):
    __tablename__ = "message"
    
    message_uuid: Mapped[str] = mapped_column(
        String(36), primary_key = True, default = lambda: str(uuid.uuid4())
    )
    match_uuid: Mapped[str] = mapped_column(
        String(36)
    )
    sender_uuid: Mapped[str] = mapped_column(
        String(36)
    )
    receiver_uuid: Mapped[str] = mapped_column(
        String(36)
    )
    message: Mapped[str] = mapped_column(
        Text, nullable = False
    )
    created: Mapped[datetime] = mapped_column(
        DateTime, default = lambda: datetime.now()
    )
    
    __table_args__ = (
        ForeignKeyConstraint(
            ["match_uuid"],
            ["match.match_uuid"]
        ),
        ForeignKeyConstraint(
            ["sender_uuid"],
            ["user.user_uuid"]
        ),
        ForeignKeyConstraint(
            ["receiver_uuid"],
            ["user.user_uuid"]
        )
    )