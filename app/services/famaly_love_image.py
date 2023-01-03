from functools import lru_cache
from fastapi import Depends
from data_acces_layer import DALFamalyLoveImage, get_DAL_famaly_love_image
from sqlalchemy.ext.asyncio import AsyncSession


class FamalyLoveImageService:
    def __init__(self, database: DALFamalyLoveImage) -> None:
        self.database = database

    async def create(
        self: 'FamalyLoveImageService',
        famaly_love_quiz: int,
        is_male: bool,
        image_path: str,
        session: AsyncSession
    ) -> None:
        pass


@lru_cache()
def get_famaly_love_image_service(
    database: DALFamalyLoveImage = Depends(get_DAL_famaly_love_image)
) -> FamalyLoveImageService:
    return FamalyLoveImageService(database)
