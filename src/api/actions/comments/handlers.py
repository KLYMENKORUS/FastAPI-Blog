from logging import getLogger
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from api.actions.posts.handlers import get_post_by_id
from api.actions.users.handlers import get_user_by_id
from api.actions.authenticate.optional import get_current_user_from_token
from api.actions.comments.models import CommentShow, CommentCreate
from api.actions.comments.optional import _create_new_comment,\
    _get_comment_by_id, _get_post_id_by_comment
from api.actions.users.models import ShowUser
from db.session import get_db

logger = getLogger(__name__)

comment_router = APIRouter()


@comment_router.post('/', response_model=CommentShow)
async def create_new_comment(
        body: CommentCreate,
        db: AsyncSession = Depends(get_db),
        current_user: ShowUser = Depends(get_current_user_from_token)
) -> CommentShow:
    try:
        user = await get_user_by_id(current_user.user_id, db)
        post = await get_post_by_id(body.post_id, db)
        return await _create_new_comment(
            body, db, current_user.user_id, user, post
        )
    except IntegrityError as err:
        logger.error(err)
        HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                      detail=f'Database error {err}')


@comment_router.get('/', response_model=CommentShow)
async def get_comment_by_id(
        comment_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: ShowUser = Depends(get_current_user_from_token)
) -> CommentShow:
    try:
        user = await get_user_by_id(current_user.user_id, db)
        post_id = await _get_post_id_by_comment(comment_id, db)
        post = await get_post_by_id(post_id, db)

        get_comment = await _get_comment_by_id(
            comment_id, db, user, post
        )

        if get_comment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f'Comment with id {comment_id} not found'
            )

        return get_comment
    except IntegrityError as err:
        logger.error(err)
        HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                      detail=f'Database error {err}')
