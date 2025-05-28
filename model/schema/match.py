from pydantic import BaseModel
from model.match import MatchStatus

class UpdateMatchStatusModel(BaseModel):
    match_uuid: str
    status: MatchStatus
