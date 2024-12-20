from decimal import Decimal
from typing import Iterable

from pydantic import BaseModel

from domain.entities.location import Location


class LocationResponseSchema(BaseModel):
    name: str
    latitude: Decimal
    longitude: Decimal

    @classmethod
    def from_entity(cls, location: Location) -> "LocationResponseSchema":
        return cls(
            name=location.name,
            latitude=location.latitude,
            longitude=location.latitude,
        )


class LocationsResponseSchema(BaseModel):
    locations: Iterable[LocationResponseSchema]

    @classmethod
    def from_entity(cls, locations: Iterable[Location]) -> "LocationsResponseSchema":
        return cls(
            locations=[
                LocationResponseSchema.from_entity(location) for location in locations
            ],
        )


class AddNewLocationRequestSchema(BaseModel):
    name: str
    latitude: Decimal
    longitude: Decimal
