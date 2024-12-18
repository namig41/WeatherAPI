from abc import abstractmethod
from typing import Protocol

from domain.value_objects.hashed_password import HashedPassword
from domain.value_objects.raw_password import RawPassword


class IPasswordHasher(Protocol):
    @abstractmethod
    def hash_password(self, password: RawPassword) -> HashedPassword: ...

    @abstractmethod
    def verify_password(
        self,
        raw_password: RawPassword,
        hashed_password: HashedPassword,
    ) -> bool: ...
