from dataclasses import (
    dataclass,
    field,
)

from domain.entities.base import BaseEntity


@dataclass
class User(BaseEntity):
    id: int = field(init=False)
    login: str
    password: str

    def validate(self):
        return super().validate()

    def __hash__(self):
        return hash(self.login)

    def __eq__(self, user: object) -> bool:
        if isinstance(user, User):
            return self.login == user.login
        return False
