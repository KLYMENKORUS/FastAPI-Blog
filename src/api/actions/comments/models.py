from pydantic import BaseModel
from datetime import datetime


# BLOCK WITH API MODELS


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""

        orm_mode = True


class CommentCreate(BaseModel):
    body: str
    post_id: int


class CommentShow(TunedModel):
    post: dict
    created: datetime
    body: str
    user: dict
