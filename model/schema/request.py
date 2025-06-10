from model.request import RequestStatus
from datetime import date, time
from pydantic import BaseModel

class CreateRequestModel(BaseModel):
    title: str
    description: str | None = None
    available_date: date | None = None
    available_start_time: time | None = None
    available_end_time: time | None = None

class UpdateRequestStatusModel(BaseModel):
    status: RequestStatus
