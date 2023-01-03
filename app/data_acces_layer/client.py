from models.database import OrmClient, OrmFamalyLoveQuiz
from sqlalchemy import asc, func, select, text
from sqlalchemy.orm import selectinload
from .abstract import AbstractDALClient
from functools import lru_cache
from sqlalchemy.ext.asyncio import AsyncSession


class DALClient(AbstractDALClient):
    async def create(
        self: 'DALClient',
        session: AsyncSession
    ) -> OrmClient:
        orm_client = OrmClient()
        session.add(orm_client)
        await session.flush()
        await session.refresh(orm_client)
        return orm_client

    async def get_by_id(
        self: 'DALClient',
        id: int,
        session: AsyncSession
    ) -> OrmClient:
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
        self: 'DALClient',
        session: AsyncSession
    ) -> int:
        count = await session.execute(
            select(
                func.count()
            )
            .select_from(OrmClient)
        )
        return count.scalar()

    async def delete_by_id(
        self: 'DALClient',
        id: int,
        session: AsyncSession
    ) -> OrmClient:
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
        return orm_client


@lru_cache()
def get_DAL_client() -> DALClient:
    return DALClient()
