from dataclasses import dataclass

from domain.entities.base import BaseEntity
from domain.interfaces.infrastructure.password_hasher import IPasswordHasher
from domain.value_objects.hashed_password import HashedPassword
from domain.value_objects.raw_password import RawPassword
from domain.value_objects.user_email import UserEmail


@dataclass
class User(BaseEntity):
    login: str
    email: UserEmail
    hashed_password: HashedPassword
    id: int | None = None

    def validate(self) -> None: ...

    @classmethod
    def create_with_raw_password(
        cls,
        login: str,
        email: UserEmail,
        raw_password: RawPassword,
        password_hasher: IPasswordHasher,
    ) -> "User":
        hashed_password: HashedPassword = password_hasher.hash_password(raw_password)
        return cls(login=login, email=email, hashed_password=hashed_password)

    def __hash__(self) -> int:
        return hash(self.login)

    def __eq__(self, user: object) -> bool:
        if isinstance(user, User):
            return self.login == user.login
        return False
