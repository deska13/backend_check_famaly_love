from sqlalchemy.ext.asyncio import AsyncSession
from models.database import OrmFamalyLoveImage
from sqlalchemy import asc, func, select, text
from sqlalchemy.orm import selectinload
from .abstract import AbstractDALFamalyLoveImage
from functools import lru_cache


class DALFamalyLoveImage(AbstractDALFamalyLoveImage):
    async def create(
        self: 'DALFamalyLoveImage',
        famaly_love_quiz_id: int,
        image_path: str,
        is_male: bool,
        session: AsyncSession
    ) -> OrmFamalyLoveImage:
        orm_famaly_love_image = OrmFamalyLoveImage(
            famaly_love_quiz_id=famaly_love_quiz_id,
            image_path=image_path,
            is_male=is_male
        )
        session.add(orm_famaly_love_image)
        await session.flush()
        await session.refresh(orm_famaly_love_image)
        return orm_famaly_love_image

    async def get_by_id(
        self: 'DALFamalyLoveImage',
        id: int,
        session: AsyncSession
    ) -> OrmFamalyLoveImage:
        orm_famaly_love_image = await session.execute(
            select(OrmFamalyLoveImage)
            .where(OrmFamalyLoveImage.id == id)
        )
        return orm_famaly_love_image.scalar()

    async def get_count(
        self: 'DALFamalyLoveImage',
        session: AsyncSession
    ) -> int:
        count_famaly_love_images = await session.execute(
            select(func.count())
            .select_from(OrmFamalyLoveImage)
        )
        return count_famaly_love_images.scalar()

    async def update_by_id(
        self: 'DALFamalyLoveImage',
        id: int,
        image_path: str,
        session: AsyncSession
    ) -> OrmFamalyLoveImage:
        orm_famaly_love_image = await self.get_by_id(id)
        if not orm_famaly_love_image:
            return None
        orm_famaly_love_image.image_path = image_path
        session.add(orm_famaly_love_image)

    async def delete_by_id(
        self: 'DALFamalyLoveImage',
        id: int,
        session: AsyncSession
    ) -> OrmFamalyLoveImage:
        orm_famaly_love_image = await session.execute(
            select(OrmFamalyLoveImage)
            .where(OrmFamalyLoveImage.id == id)
        )
        if not orm_famaly_love_image:
            return None
        await session.delete(orm_famaly_love_image)


@lru_cache()
def get_DAL_famaly_love_image() -> DALFamalyLoveImage:
    return DALFamalyLoveImage()
