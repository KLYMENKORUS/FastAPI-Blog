from logging import getLogger

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.actions.authenticate.optional import get_current_user_from_token
from api.actions.posts.models import ShowPost, PostCreate, \
    DeletePostResponse, UpdatePostResponse, UpdatePostRequest
from api.actions.posts.optional import _create_new_post, \
    _delete_post, _get_post_by_id, _update_post, _get_owner_id, _post_by_id
from api.actions.users.handlers import get_user_by_id
from api.actions.users.models import ShowUser
from db.session import get_db

logger = getLogger(__name__)

post_route = APIRouter()


@post_route.post('/', response_model=ShowPost)
async def create_new_post(
        body: PostCreate,
        db: AsyncSession = Depends(get_db),
        current_user: ShowUser = Depends(get_current_user_from_token)
) -> ShowPost:
    try:
        return await _create_new_post(body, db, current_user.user_id)
    except IntegrityError as err:
        logger.error(err)
        HTTPException(status_code=503, detail=f'Database error {err}')


@post_route.delete('/', response_model=DeletePostResponse)
async def delete_post(
        post_id: int, db: AsyncSession = Depends(get_db),
        current_user: ShowUser = Depends(get_current_user_from_token)
) -> DeletePostResponse:
    current_post = await _post_by_id(post_id, db)
    if current_post.owner_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='You are not the author of this post and do not have permission to delete'
        )
    post_deleted_id = await _delete_post(post_id, db)
    if post_deleted_id is None:
        raise HTTPException(
            status_code=404, detail=f'Post with id {post_id} not found'
        )
    return DeletePostResponse(
        post_deleted_id=post_deleted_id, status='post successfully delete'
    )


@post_route.get('/', response_model=ShowPost)
async def get_post_by_id(
        post_id: int, db: AsyncSession = Depends(get_db)
) -> ShowPost:
    owner_id = await _get_owner_id(post_id, db)
    owner = await get_user_by_id(owner_id, db)
    get_post = await _get_post_by_id(post_id, db, owner)
    if get_post is None:
        raise HTTPException(
            status_code=404, detail=f'Post with id {post_id} not found'
        )
    return get_post


@post_route.patch('/', response_model=UpdatePostResponse)
async def update_post(
        post_id: int, body: UpdatePostRequest,
        db: AsyncSession = Depends(get_db),
        current_user: ShowUser = Depends(get_current_user_from_token)
) -> UpdatePostResponse:
    current_post = await _post_by_id(post_id, db)
    if current_post.owner_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='You are not the author of this post and do not have permission to update'
        )

    updated_post_params = body.dict(exclude_none=True)
    if updated_post_params == {}:
        raise HTTPException(
            status_code=422,
            detail='At least one parameter for users update '
                   'info should be provided'
        )
    post = await _post_by_id(post_id, db)
    if post is None:
        raise HTTPException(
            status_code=404, detail=f'Post with id {post_id} not found'
        )
    updated_post = await _update_post(updated_post_params, post_id, db)
    return UpdatePostResponse(
        updated_post_id=updated_post,
        updated_data=body.dict()
    )


