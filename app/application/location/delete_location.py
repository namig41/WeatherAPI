from dataclasses import dataclass

from application.common.interactor import Interactor
from application.location.dto import LocationDTO
from infrastructure.repository.base import BaseUserLocationRepository


@dataclass
class DeleteLocationInteractor(Interactor[LocationDTO, None]):
    locations_repository: BaseUserLocationRepository

    async def __call__(self, location_dto: LocationDTO) -> None:
        await self.locations_repository.delete_location_by_name(
            user=location_dto.user,
            name=location_dto.name,
        )
