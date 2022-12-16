from ._engine import _postgres_async_session
from models.database import OrmClient, OrmFamalyLoveQuiz
from sqlalchemy import asc, func, select, text
from sqlalchemy.orm import selectinload
from .abstract import AbstractDALClient
from functools import lru_cache


class DALClient(AbstractDALClient):
    async def create(
        self: 'DALClient'
    ) -> OrmClient:
        async with _postgres_async_session() as session:
            orm_client = OrmClient()
            session.add(orm_client)
            await session.commit()
            await session.refresh(orm_client)
            return await self.get_by_id(orm_client.id)


    async def get_by_id(
        self: 'DALClient',
        id: int
    ) -> OrmClient:
        async with _postgres_async_session() as session:
            orm_client = await session.execute(
                select(OrmClient)
                .options(
                    selectinload(OrmClient.famaly_love_quizes)
                    .options(
                        selectinload(OrmFamalyLoveQuiz.images)
                    )
                )
                .options(selectinload(OrmClient.orders))
                .where(OrmClient.id == id)
            )
            return orm_client.scalar()


    async def get_count(
        self: 'DALClient'
    ) -> int:
        async with _postgres_async_session() as session:
            count = await session.execute(
                select(
                    func.count()
                )
                .select_from(OrmClient)
            )
            return count.scalar()


    async def delete_by_id(
        self: 'DALClient',
        id: int
    ) -> OrmClient:
        async with _postgres_async_session() as session:
            orm_client = await session.execute(
                select(OrmClient)
                .options(
                    selectinload(OrmClient.famaly_love_quizes)
                    .options(
                        selectinload(OrmFamalyLoveQuiz.images)
                    )
                )
                .where(OrmClient.id == id)
            )
            if not orm_client:
                return None
            await session.delete(orm_client)
            await session.commit()
            return orm_client


@lru_cache()
def get_DAL_client() -> DALClient:
    return DALClient()
