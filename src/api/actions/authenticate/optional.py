from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

import settings
from api.actions.users.hashing import Hasher
from api.actions.users.models import ShowUser
from api.actions.users.optional import _get_all_post
from db.dal import UserDAL
from db.models import User
from db.session import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login/token')


async def _get_user_by_email(email: str, db: AsyncSession) -> User | None:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            return await user_dal.get_user_by_email(
                email=email
            )


async def authenticate_user(email: str, password: str, db: AsyncSession) -> User | None:
    user = await _get_user_by_email(email, db)
    if user is None:
        return
    if not Hasher.verify_password(password, user.hashed_password):
        return
    return user


async def get_current_user_from_token(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)) -> ShowUser | None:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials'
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get('sub')
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await _get_user_by_email(email, db)
    posts = await _get_all_post(user.id, db)
    if user is None:
        raise credentials_exception
    return ShowUser(
        user_id=user.id,
        name=user.name,
        surname=user.surname,
        email=user.email,
        is_active=user.is_active,
        posts=posts
    )
