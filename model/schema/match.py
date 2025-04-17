from pydantic import BaseModel
from model.match import MatchStatus

class CreateMatchModel(BaseModel):
    request_uuid: str
    youth_uuid: str

class UpdateMatchStatusModel(BaseModel):
    match_uuid: str
    status: MatchStatus
