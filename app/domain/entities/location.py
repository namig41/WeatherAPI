from dataclasses import dataclass
from decimal import Decimal

from domain.entities.base import BaseEntity


@dataclass
class Location(BaseEntity):
    name: str
    latitude: Decimal
    longitude: Decimal
    id: int | None = None
    user_id: int | None = None

    def validate(self) -> None: ...

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, location: object) -> bool:
        if isinstance(location, Location):
            return self.name == location.name
        return False
