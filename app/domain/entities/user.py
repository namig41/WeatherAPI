from dataclasses import (
    dataclass,
    field,
)

from domain.entities.base import BaseEntity
from domain.interfaces.infrastructure.password_hasher import IPasswordHasher
from domain.value_objects.hashed_password import HashedPassword
from domain.value_objects.raw_password import RawPassword


@dataclass
class User(BaseEntity):
    id: int = field(init=False)
    login: str
    hashed_password: HashedPassword

    def validate(self):
        return super().validate()

    @classmethod
    def create_with_raw_password(
        cls,
        login: str,
        raw_password: RawPassword,
        password_hasher: IPasswordHasher,
    ) -> "User":
        hashed_password: HashedPassword = password_hasher.hash_password(raw_password)
        return cls(login=login, hashed_password=hashed_password)

    def __hash__(self):
        return hash(self.login)

    def __eq__(self, user: object) -> bool:
        if isinstance(user, User):
            return self.login == user.login
        return False
