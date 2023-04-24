from sqlalchemy.ext.asyncio import AsyncSession

from api.actions.posts.models import PostCreate, ShowPost, ShowPostID
from api.actions.users.models import ShowUser
from db.dal import PostDAL


async def _create_new_post(body: PostCreate, db: AsyncSession,
                           current_user: int) -> ShowPost:
    async with db as session:
        async with session.begin():
            post_dal = PostDAL(session)
            post = await post_dal.create_post(
                title=body.title,
                body=body.body,
                owner_id=current_user
            )
            return ShowPost(
                post_id=post.id,
                title=post.title,
                body=post.body,
                created=post.created,
                owner_id=post.owner_id
            )


async def _delete_post(post_id: int, db: AsyncSession) -> int | None:
    async with db as session:
        async with session.begin():
            post_dal = PostDAL(session)
            delete_post = await post_dal.delete_post(
                post_id=post_id
            )
            return delete_post


async def _get_post_by_id(post_id: int, db: AsyncSession,
                          owner: ShowUser) -> ShowPost | None:
    async with db as session:
        async with session.begin():
            post_dal = PostDAL(session)
            get_post = await post_dal.get_post_by_id(
                post_id=post_id
            )
            if get_post is not None:
                return ShowPost(
                    post_id=get_post.id,
                    title=get_post.title,
                    body=get_post.body,
                    created=get_post.created,
                    owner=owner
                )


async def _post_by_id(post_id: int, db: AsyncSession) -> ShowPostID | None:
    async with db as session:
        async with session.begin():
            post_dal = PostDAL(session)
            get_post = await post_dal.get_post_by_id(
                post_id=post_id
            )
            if get_post is not None:
                return ShowPostID(
                    post_id=get_post.id,
                    title=get_post.title,
                    body=get_post.body,
                    created=get_post.created,
                    owner_id=get_post.owner_id
                )


async def _get_owner_id(post_id: int, db: AsyncSession) -> int | None:
    async with db as session:
        async with session.begin():
            post_dal = PostDAL(session)
            return await post_dal.get_owner_id(post_id=post_id)


async def _update_post(updated_params: dict, post_id: int, db: AsyncSession) -> int | None:
    async with db as session:
        async with session.begin():
            post_dal = PostDAL(session)
            updated_post = await post_dal.update_post(
                post_id,
                **updated_params
            )
            return updated_post