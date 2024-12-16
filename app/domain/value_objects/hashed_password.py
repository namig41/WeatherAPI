from dataclasses import dataclass

from domain.value_objects.base import BaseValueObject


@dataclass(frozen=True)
class HashedPassword(BaseValueObject[str]):

    def validate(self):
        return True
