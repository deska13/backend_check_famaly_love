from ._engine import _postgres_async_session
from models.database import OrmFamalyLoveImage
from sqlalchemy import asc, func, select, text
from sqlalchemy.orm import selectinload
from .abstract import AbstractDALFamalyLoveImage


class DALFamalyLoveImage(AbstractDALFamalyLoveImage):
    async def create(
        self: 'DALFamalyLoveImage',
        image_path: str
    ) -> OrmFamalyLoveImage:
        async with _postgres_async_session() as session:
            orm_famaly_love_image = OrmFamalyLoveImage(
                image_path=image_path,
            )
            session.add(orm_famaly_love_image)
            await session.commit()
            await session.refresh(orm_famaly_love_image)
            return await self.get_by_id(orm_famaly_love_image.id)


    async def get_by_id(
        self: 'DALFamalyLoveImage',
        id: int
    ) -> OrmFamalyLoveImage:
        async with _postgres_async_session() as session:
            orm_famaly_love_image = await session.execute(
                select(OrmFamalyLoveImage)
                .where(OrmFamalyLoveImage.id == id)
            )
            return orm_famaly_love_image.scalar()


    async def get_count(
        self: 'DALFamalyLoveImage'
    ) -> int:
        async with _postgres_async_session() as session:
            count_famaly_love_images = await session.execute(
                select(func.count())
                .select_from(OrmFamalyLoveImage)
            )
            return count_famaly_love_images.scalar()


    async def update_by_id(
        self: 'DALFamalyLoveImage',
        id: int, 
        image_path: str
    ) -> OrmFamalyLoveImage:
        async with _postgres_async_session() as session:
            orm_famaly_love_image = await self.get_by_id(id)
            if not orm_famaly_love_image:
                return None
            orm_famaly_love_image.image_path = image_path
            session.add(orm_famaly_love_image)
            await session.commit()
            return await self.get_by_id(id)


    async def delete_by_id(
        self: 'DALFamalyLoveImage',
        id: int
    ) -> OrmFamalyLoveImage:
        async with _postgres_async_session() as session:
            orm_famaly_love_image = await session.execute(
                select(OrmFamalyLoveImage)
                .where(OrmFamalyLoveImage.id == id)
            )
            if not orm_famaly_love_image:
                return None
            await session.delete(orm_famaly_love_image)
            await session.commit()
            return orm_famaly_love_image
