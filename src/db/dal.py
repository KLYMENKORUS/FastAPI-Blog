from typing import List

from sqlalchemy import update, and_, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import User, Post, Comment


# Block business context
class UserDAL:
    """Data Access layer for operating users info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
            self, name: str, surname: str, email: str,
            hashed_password: str
    ) -> User:
        new_user = User(
            name=name,
            surname=surname,
            email=email,
            hashed_password=hashed_password
        )
        self.db_session.add(new_user)
        await self.db_session.flush()

        return new_user

    async def delete_user(self, user_id: int) -> int | None:
        query = (
            update(User)
            .where(and_(User.id == user_id, User.is_active == True))
            .values(is_active=False).returning(User.id)
        )
        result = await self.db_session.execute(query)
        delete_user_id_row = result.fetchone()
        if delete_user_id_row is not None:
            return delete_user_id_row[0]

    async def get_user_by_id(self, user_id: int) -> User | None:
        query = (
            select(User).where(and_(User.id == user_id))
        )
        result = await self.db_session.execute(query)
        user_row = result.fetchone()
        if user_row is not None:
            return user_row[0]

    async def get_all_post_by_user_id(self, user_id: int) -> List[Post] | None:
        query = (
            select(Post).where(and_(Post.owner_id == user_id))
        )
        result = await self.db_session.execute(query)
        all_posts = result.fetchall()
        if all(all_posts) is not None:
            return [post[0] for post in all_posts]

    async def update_user(self, user_id: int, **kwargs) -> int | None:
        query = (
            update(User).
            where(and_(User.id == user_id, User.is_active == True)).
            values(kwargs).returning(User.id)
        )
        result = await self.db_session.execute(query)
        update_user_id_row = result.fetchone()
        if update_user_id_row is not None:
            return update_user_id_row[0]

    async def get_user_by_email(self, email: str) -> User | None:
        query = (
            select(User).where(and_(User.email == email))
        )
        result = await self.db_session.execute(query)
        user_row = result.fetchone()
        if user_row is not None:
            return user_row[0]
        

class PostDAL:
    """Data Access layer for operating post info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_post(
            self, title: str, body: str, owner_id: int
    ) -> Post:
        new_post = Post(
            title=title,
            body=body,
            owner_id=owner_id
        )
        self.db_session.add(new_post)
        await self.db_session.flush()

        return new_post

    async def delete_post(self, post_id: int) -> Post | None:
        query = delete(Post).\
            where(and_(Post.id == post_id)).returning(Post.id)
        result = await self.db_session.execute(query)
        deleted_post_id_row = result.fetchone()
        if deleted_post_id_row is not None:
            return deleted_post_id_row[0]

    async def get_post_by_id(self, post_id: int) -> Post | None:
        query = (
            select(Post).where(and_(Post.id == post_id))
        )
        result = await self.db_session.execute(query)
        post_row = result.fetchone()
        if post_row is not None:
            return post_row[0]

    async def get_owner_id(self, post_id: int) -> int | None:
        query = (
            select(Post.owner_id).where(and_(Post.id == post_id))
        )
        result = await self.db_session.execute(query)
        owner_id = result.fetchone()
        return owner_id[0] if owner_id else None

    async def update_post(self, post_id: int, **kwargs) -> Post | None:
        query = (
            update(Post).
            where(and_(Post.id == post_id)).
            values(kwargs).returning(Post.id)
        )
        result = await self.db_session.execute(query)
        updated_post = result.fetchone()
        if updated_post is not None:
            return updated_post[0]


class CommentsDAL:
    """Data Access layer for operating comment info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_comment(
            self, post_id: int, user_id: int, body: str
    ) -> Comment:
        new_comment = Comment(
            body=body,
            post_id=post_id,
            user_id=user_id
        )
        self.db_session.add(new_comment)
        await self.db_session.flush()

        return new_comment

    async def get_comment_by_id(self, comment_id: int) -> Comment | None:
        query = (
            select(Comment).where(and_(Comment.id == comment_id))
        )
        result = await self.db_session.execute(query)
        get_comment_id = result.fetchone()
        if get_comment_id is not None:
            return get_comment_id[0]

    async def get_post_id_by_comment(self, comment_id: int) -> int | None:
        query = (
            select(Comment.post_id).where(and_(Comment.id == comment_id))
        )
        result = await self.db_session.execute(query)
        id_post = result.fetchone()
        if id_post is not None:
            return id_post[0]