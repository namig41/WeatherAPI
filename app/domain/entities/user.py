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
