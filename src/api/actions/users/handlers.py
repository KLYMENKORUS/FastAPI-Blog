from logging import getLogger

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.actions.users.models import UserCreate, ShowUser, \
    DeleteUserResponse, UpdateUserRequest, UpdateUserResponse
from api.actions.users.optional import _create_new_user, _delete_user,\
    _get_user_by_id, _update_user, _get_all_post
from api.actions.authenticate.optional import get_current_user_from_token
from db.models import User
from db.session import get_db

logger = getLogger(__name__)

user_route = APIRouter()


@user_route.post('/', response_model=ShowUser)
async def create_new_user(
        body: UserCreate, db: AsyncSession = Depends(get_db)
) -> ShowUser:
    try:
        return await _create_new_user(body, db)
    except IntegrityError as err:
        logger.error(err)
        HTTPException(status_code=503, detail=f'Database error {err}')


@user_route.delete('/', response_model=DeleteUserResponse)
async def delete_user(
        current_user: User = Depends(get_current_user_from_token),
        db: AsyncSession = Depends(get_db)) -> DeleteUserResponse:
    deleted_user_id = await _delete_user(current_user.user_id, db)
    if deleted_user_id is None:
        raise HTTPException(
            status_code=404, detail=f'User with id {current_user.user_id} not found'
        )
    return DeleteUserResponse(deleted_user_id=deleted_user_id)


@user_route.get('/', response_model=ShowUser)
async def get_user_by_id(
        user_id: int, db: AsyncSession = Depends(get_db)
) -> ShowUser:
    posts = await _get_all_post(user_id, db)
    get_user = await _get_user_by_id(user_id, db, posts)
    if get_user is None:
        raise HTTPException(
            status_code=404, detail=f'User with id {user_id} not found'
        )
    return get_user


@user_route.patch('/', response_model=UpdateUserResponse)
async def update_user_by_id(
        body: UpdateUserRequest,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)) -> UpdateUserResponse:
    updated_user_params = body.dict(exclude_none=True)
    if updated_user_params == {}:
        raise HTTPException(
            status_code=422,
            detail='At least one parameter for users update '
                   'info should be provided'
        )
    user = await _get_user_by_id(current_user.user_id, db)
    if user is None:
        raise HTTPException(
            status_code=404, detail=f'User with id {user} not found'
        )
    updated_user = await _update_user(updated_user_params, user.user_id, db)
    return UpdateUserResponse(
        updated_user_id=updated_user,
        updated_data=body.dict()
    )
