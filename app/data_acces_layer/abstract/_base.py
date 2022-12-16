from abc import ABC, abstractmethod
from typing import Optional


class BaseAbstractDataAccessLayer(ABC):
    @abstractmethod
    async def get_by_id(self, id: int) -> None:
        pass

    @abstractmethod
    async def get_count(self) -> int:
        pass

    @abstractmethod
    async def delete_by_id(self, id: int) -> None:
        pass
