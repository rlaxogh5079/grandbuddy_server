from pydantic import BaseModel
from model.request import RequestStatus

class CreateRequestModel(BaseModel):
    title: str
    description: str | None = None

class UpdateRequestStatusModel(BaseModel):
    status: RequestStatus
