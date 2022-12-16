from abc import abstractmethod
from typing import Optional

from ._base import BaseAbstractDataAccessLayer


class AbstractDALClient(BaseAbstractDataAccessLayer):
    @abstractmethod
    async def create(
        self: 'AbstractDALClient'
    ) -> int:
        pass
