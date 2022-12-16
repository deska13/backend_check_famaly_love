from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from core import PostgresSetting


_engine = create_async_engine(
    PostgresSetting().postgres_async_connect,
    echo=True,
)


_postgres_async_session = sessionmaker(
    _engine, expire_on_commit=False, class_=AsyncSession
)

__all__ = ["_postgres_async_session"]