from dataclasses import dataclass
from typing import Iterable

from application.common.interactor import Interactor
from application.location.dto import FiltersLocationDTO
from domain.entities.location import Location
from infrastructure.repository.base import BaseUserLocationRepository


@dataclass
class GetAllLocationInteractor(Interactor[FiltersLocationDTO, Iterable[Location]]):
    locations_repository: BaseUserLocationRepository

    async def __call__(self, filters_location_dto: FiltersLocationDTO) -> Iterable[Location]:
        locations: Iterable[Location] = (
            await self.locations_repository.get_all_location(
                user=filters_location_dto.location.user,
                filters=filters_location_dto.filters,
            )
        )

        return locations
