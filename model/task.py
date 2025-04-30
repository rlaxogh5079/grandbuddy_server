from sqlalchemy import String, DateTime, Text, ForeignKeyConstraint, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from model.base_class import Base
from enum import Enum
import uuid

class TaskStatus(Enum):
    pending = 0   # 대기
    in_progress = 1  # 진행
    completed = 2  # 완료

class Task(Base):
    __tablename__ = "task"
    
    task_uuid: Mapped[str] = mapped_column(
        String(36), primary_key = True, default = lambda: str(uuid.uuid4())
    )
    user_uuid: Mapped[str] = mapped_column(
        String(36)
    )
    title: Mapped[str] = mapped_column(
        Text, nullable = False
    )
    description: Mapped[str] = mapped_column(
        Text, nullable = True, default = None
    )
    status: Mapped[TaskStatus] = mapped_column(
        SQLEnum(TaskStatus), default = lambda: TaskStatus.pending
    )
    created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    dueDate: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable = False
    )
    
    __talbe_args__ = (
        ForeignKeyConstraint(
            ["user_uuid"],
            ["user.user_uuid"]
        )
    )