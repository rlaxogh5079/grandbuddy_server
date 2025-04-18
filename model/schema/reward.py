from pydantic import BaseModel

class CreateRewardModel(BaseModel):
    youth_uuid: str
    points: int
    description: str | None = None
