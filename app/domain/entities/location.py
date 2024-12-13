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
