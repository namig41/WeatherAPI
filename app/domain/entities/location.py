from dataclasses import (
    dataclass,
    field,
)
from decimal import Decimal

from domain.entities.base import BaseEntity


@dataclass
class Location(BaseEntity):
    id: int = field(init=False)
    name: str
    latitude: Decimal
    longitude: Decimal

    def validate(self):
        return super().validate()

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, location: object) -> bool:
        if isinstance(location, Location):
            return self.name == location.name
        return False
