from abc import ABC, abstractmethod
from typing import Optional


class BaseAbstractDataAccessLayer(ABC):
    @abstractmethod
    async def get_by_id(self, id: int) -> None:
        pass
