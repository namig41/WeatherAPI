from infrastructure.exceptions.auth import PasswordMismatchException

from domain.interfaces.infrastructure.password_hasher import BasePasswordHasher
from domain.value_objects.hashed_password import HashedPassword
from domain.value_objects.raw_password import RawPassword


class SimplePasswordHasher(BasePasswordHasher):
    def hash_password(self, password: RawPassword) -> HashedPassword:
        return HashedPassword(password.value)

    def verify_password(
        self,
        raw_password: RawPassword,
        hashed_password: HashedPassword,
    ) -> None:
        if raw_password.value != hashed_password.value:
            raise PasswordMismatchException()
