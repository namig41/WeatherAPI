from passlib.context import CryptContext

from domain.interfaces.infrastructure.password_hasher import IPasswordHasher
from domain.value_objects.hashed_password import HashedPassword
from domain.value_objects.raw_password import RawPassword


class SimplePasswordHasher(IPasswordHasher):
    def hash_password(self, password: RawPassword) -> HashedPassword:
        return HashedPassword(password.value)

    def verify_password(
        self,
        raw_password: RawPassword,
        hashed_password: HashedPassword,
    ) -> bool:
        return raw_password.value == hashed_password.value


class SHA256PasswordHasher(IPasswordHasher):

    def __init__(self):
        self.pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

    def hash_password(self, password: RawPassword) -> HashedPassword:
        return HashedPassword(self.pwd_context.hash(password.value))

    def verify_password(
        self,
        raw_password: RawPassword,
        hashed_password: HashedPassword,
    ) -> bool:
        return self.pwd_context.verify(raw_password.value, hashed_password.value)
