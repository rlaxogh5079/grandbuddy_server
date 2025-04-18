from pydantic import BaseModel

class CreateReviewModel(BaseModel):
    request_uuid: str
    user_uuid: str
    rating: float
    content: str | None = None

class UpdateReviewModel(BaseModel):
    rating: float
    content: str | None = None