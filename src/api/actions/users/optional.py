from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from api.actions.posts.models import ShowPostID
from api.actions.users.hashing import Hasher
from api.actions.users.models import UserCreate, ShowUser
from db.dal import UserDAL


async def _create_new_user(body: UserCreate, db: AsyncSession) -> ShowUser:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                name=body.name,
                surname=body.surname,
                email=body.email,
                hashed_password=Hasher.get_password_hash(body.password)
            )
            return ShowUser(
                user_id=user.id,
                name=user.name,
                surname=user.surname,
                email=user.email,
                is_active=user.is_active
            )


async def _delete_user(user_id: int, db: AsyncSession) -> int | None:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            delete_user = await user_dal.delete_user(
                user_id=user_id
            )
            return delete_user


async def _update_user(updated_user_params: dict, user_id: int, db: AsyncSession) -> int | None:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            update_user = await user_dal.update_user(
                user_id=user_id,
                **updated_user_params
            )
            return update_user


async def _get_user_by_id(user_id: int, db: AsyncSession,
                          all_post: list = None) -> ShowUser | None:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            get_user = await user_dal.get_user_by_id(
                user_id=user_id
            )
            if get_user is not None:
                return ShowUser(
                    user_id=get_user.id,
                    name=get_user.name,
                    surname=get_user.surname,
                    email=get_user.email,
                    is_active=get_user.is_active,
                    posts=all_post
                )


async def _get_all_post(user_id: int, db: AsyncSession) -> List[ShowPostID]:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            all_post = await user_dal.get_all_post_by_user_id(
                user_id=user_id
            )
            if all(all_post) is not None:
                return [
                    ShowPostID(
                        post_id=post.id,
                        title=post.title,
                        body=post.body,
                        created=post.created,
                        owner_id=post.owner_id
                    ) for post in all_post]

