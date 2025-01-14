from dataclasses import dataclass
from typing import Iterable

from application.common.interactor import Interactor
from application.location.dto import LocationDTO
from domain.entities.location import Location
from infrastructure.repository.base import BaseUserLocationRepository
from infrastructure.repository.filters import RepositoryFilters


@dataclass
class GetAllLocationInteractor(Interactor[LocationDTO, Iterable[Location]]):
    locations_repository: BaseUserLocationRepository

    async def __call__(self, location_dto: LocationDTO) -> Iterable[Location]:
        locations: Iterable[Location] = (
            await self.locations_repository.get_all_location(
                user=location_dto.user,
                filters=RepositoryFilters(),
            )
        )

        return locations
