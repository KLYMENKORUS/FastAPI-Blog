from datetime import datetime
from typing import Optional

from pydantic import BaseModel, constr


# BLOCK WITH API MODELS


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""

        orm_mode = True


class ShowPost(TunedModel):
    post_id: int
    title: str
    body: str
    created: datetime
    owner: dict


class ShowPostID(TunedModel):
    post_id: int
    title: str
    body: str
    created: datetime
    owner_id: int


class PostCreate(BaseModel):
    title: str
    body: str


class DeletePostResponse(BaseModel):
    post_deleted_id: int
    status: str


class UpdatePostRequest(BaseModel):
    title: Optional[constr(min_length=1)]
    body: Optional[constr(min_length=1)]


class UpdatePostResponse(BaseModel):
    updated_post_id: int
    updated_data: dict