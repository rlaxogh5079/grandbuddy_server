from sqlalchemy import String, DateTime, Text, ForeignKeyConstraint, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from model.base import Base
from enum import Enum
import uuid

class TaskStatus(Enum):
    pending = 0 # 진행 중
    completed = 1 # 완료

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
        DateTime, default = lambda: datetime.now()
    )
    dueDate: Mapped[datetime] = mapped_column(
        DateTime, nullable = False
    )
    
    __talbe_args__ = (
        ForeignKeyConstraint(
            ["user_uuid"],
            ["user.user_uuid"]
        )
    )