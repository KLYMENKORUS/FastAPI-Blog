import re
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, validator, constr


# BLOCK WITH API MODELS

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""

        orm_mode = True


class ShowUser(TunedModel):
    user_id: int
    name: str
    surname: str
    email: EmailStr
    is_active: bool
    posts: list


class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str

    @validator('name')
    def validate_name(cls, value):
        if not isinstance(value, str) or not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422,
                detail='Name should contains only letters'
            )
        return value

    @validator('surname')
    def validate_surname(cls, value):
        if not isinstance(value, str) or not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422,
                detail='Surname should contains only letters'
            )
        return value


class DeleteUserResponse(BaseModel):
    deleted_user_id: int


class UpdateUserResponse(BaseModel):
    updated_user_id: int
    updated_data: dict


class UpdateUserRequest(BaseModel):
    name: Optional[constr(min_length=1)]
    surname: Optional[constr(min_length=1)]
    email: Optional[EmailStr]

    @validator('name')
    def validate_name(cls, value):
        if not isinstance(value, str) or not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422,
                detail='Name should contains only letters'
            )
        return value

    @validator('surname')
    def validate_surname(cls, value):
        if not isinstance(value, str) or not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422,
                detail='Surname should contains only letters'
            )
        return value