from functools import lru_cache
from fastapi import Depends
from data_acces_layer import DALClient, get_DAL_client
from models.business import BusinessClient
from models.database import OrmClient
from sqlalchemy.ext.asyncio import AsyncSession


class ClientService:
    def __init__(
        self: 'ClientService',
        database: DALClient
    ) -> None:
        self.database = database

    async def create(
        self: 'ClientService',
        session: AsyncSession
    ) -> BusinessClient:
        orm_client = await self.database.create(session)
        return BusinessClient.from_orm(orm_client)

    async def get_by_id(
        self: 'ClientService',
        id: int,
        session: AsyncSession
    ) -> BusinessClient:
        orm_client = await self.database.get_by_id(id, session)
        return BusinessClient.from_orm(orm_client)


@lru_cache()
def get_client_service(
    database: DALClient = Depends(get_DAL_client)
) -> ClientService:
    return ClientService(database)
