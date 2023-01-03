from sqlalchemy.ext.asyncio import AsyncSession
from ._engine import _postgres_async_session


async def get_session() -> AsyncSession:
    async with _postgres_async_session() as session:
        yield session
