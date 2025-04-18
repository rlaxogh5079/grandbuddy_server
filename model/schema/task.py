from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CreateTaskModel(BaseModel):
    title: str
    description: str | None = None
    dueDate: datetime

class UpdateTaskModel(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    dueDate: Optional[datetime] = None