from dataclasses import dataclass

from application.common.interactor import Interactor
from application.location.dto import LocationDTO
from domain.entities.location import Location
from infrastructure.repository.base import BaseUserLocationRepository


@dataclass
class GetLocationInteractor(Interactor[LocationDTO, Location]):
    locations_repository: BaseUserLocationRepository

    async def __call__(self, location_dto: LocationDTO) -> Location:
        location: Location = await self.locations_repository.get_location_by_name(
            user=location_dto.user,
            name=location_dto.name,
        )

        return location
