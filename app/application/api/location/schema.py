from decimal import Decimal
from typing import Iterable

from pydantic import BaseModel

from domain.entities.location import Location


class GetLocationResponseSchema(BaseModel):
    name: str
    latitude: Decimal
    longitude: Decimal

    @classmethod
    def from_entity(cls, location: Location) -> "GetLocationResponseSchema":
        return cls(
            name=location.name, latitude=location.latitude, longitude=location.latitude,
        )


class GetLocationsResponseSchema(BaseModel):
    locations: Iterable[GetLocationResponseSchema]

    @classmethod
    def from_entity(cls, locations: Iterable[Location]) -> "GetLocationsResponseSchema":
        return cls(
            locations=[
                GetLocationResponseSchema.from_entity(location)
                for location in locations
            ],
        )


class AddNewLocationRequestSchema(BaseModel):
    name: str
    latitude: Decimal
    longitude: Decimal
