from dataclasses import dataclass

from application.common.interactor import Interactor
from application.location.dto import LocationDTO
from domain.entities.location import Location
from infrastructure.repository.base import BaseUserLocationRepository


@dataclass
class AddLocationInteractor(Interactor[LocationDTO, Location]):
    locations_repository: BaseUserLocationRepository

    async def __call__(self, location_dto: LocationDTO) -> Location:
        location: Location = Location(
            location_dto.name,
            location_dto.latitude,
            location_dto.longitude,
        )

        await self.locations_repository.add_location(location_dto.user, location)
        return location
