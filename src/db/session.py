from typing import Generator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker

import settings

# create async engine
engine = create_async_engine(settings.DATABASE_URL, future=True, echo=True)

# create session
async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> Generator:
    """Dependency for getting async setting"""

    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()
