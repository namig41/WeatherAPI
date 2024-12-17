from dataclasses import dataclass

from domain.interfaces.infrastructure.password_hasher import BasePasswordHasher
from domain.value_objects.hashed_password import HashedPassword
from domain.value_objects.raw_password import RawPassword


@dataclass
class SimplePasswordHasher(BasePasswordHasher):
    def hash_password(self, password: RawPassword) -> HashedPassword:
        return HashedPassword(password.value)

    def verify_password(
        self,
        raw_password: RawPassword,
        hashed_password: HashedPassword,
    ) -> bool:
        return raw_password.value == hashed_password.value
