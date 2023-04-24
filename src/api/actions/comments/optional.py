from sqlalchemy.ext.asyncio import AsyncSession

from api.actions.comments.models import CommentCreate, CommentShow
from api.actions.posts.models import ShowPost
from api.actions.users.models import ShowUser
from db.dal import CommentsDAL


async def _create_new_comment(body: CommentCreate, db: AsyncSession,
                              current_user: int,
                              data_current_user: ShowUser,
                              data_current_post: ShowPost) -> CommentShow:
    async with db as session:
        async with session.begin():
            comment_dal = CommentsDAL(session)
            comment = await comment_dal.create_comment(
                post_id=body.post_id,
                body=body.body,
                user_id=current_user
            )
            return CommentShow(
                post=data_current_post,
                created=comment.created,
                body=comment.body,
                user=data_current_user
            )


async def _get_post_id_by_comment(comment_id: int, db: AsyncSession) -> int:
    async with db as session:
        async with session.begin():
            comment_dal = CommentsDAL(session)
            id_post = await comment_dal.get_post_id_by_comment(comment_id)
            return id_post


async def _get_comment_by_id(
        comment_id: int, db: AsyncSession,
        data_user_by_comment: ShowUser,
        post: ShowPost
) -> CommentShow:
    async with db as session:
        async with session.begin():
            comment_dal = CommentsDAL(session)
            get_comment = await comment_dal.get_comment_by_id(
                comment_id=comment_id
            )
            if get_comment is not None:
                return CommentShow(
                    post=post,
                    created=get_comment.created,
                    body=get_comment.body,
                    user=data_user_by_comment
                )
