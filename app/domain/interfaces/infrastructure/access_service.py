from abc import abstractmethod
from typing import Protocol

from domain.value_objects.raw_password import RawPassword


class BaseAccessService(Protocol):
    @abstractmethod
    async def authorize(self, login: str, raw_password: RawPassword) -> None: ...
