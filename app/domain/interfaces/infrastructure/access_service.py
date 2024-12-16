from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from domain.value_objects.raw_password import RawPassword


@dataclass
class BaseAccessService(ABC):
    @abstractmethod
    async def authorize(self, login: str, raw_password: RawPassword) -> None: ...
