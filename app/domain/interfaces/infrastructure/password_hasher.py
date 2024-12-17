from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from domain.value_objects.hashed_password import HashedPassword
from domain.value_objects.raw_password import RawPassword


@dataclass
class BasePasswordHasher(ABC):
    @abstractmethod
    def hash_password(self, password: RawPassword) -> HashedPassword: ...

    @abstractmethod
    def verify_password(
        self,
        raw_password: RawPassword,
        hashed_password: HashedPassword,
    ) -> bool: ...
