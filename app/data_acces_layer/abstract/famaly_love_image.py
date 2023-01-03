from abc import abstractmethod
from typing import Optional

from ._base import BaseAbstractDataAccessLayer


class AbstractDALFamalyLoveImage(BaseAbstractDataAccessLayer):
    @abstractmethod
    async def create(
        self: 'AbstractDALFamalyLoveImage',
        image_path: str
    ) -> None:
        pass

    # @abstractmethod
    # async def update_by_id(
    #     self: 'AbstractDALFamalyLoveQuiz',
    #     id: int,
    #     image_path: str
    # ) -> None:
    #     pass
