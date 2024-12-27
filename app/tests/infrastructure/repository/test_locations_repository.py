import pytest
from infrastructure.exceptions.repository import LocationNotFoundException
from infrastructure.repository.base import BaseLocationRepository
from punq import Container

from domain.entities.location import Location
from tests.fixtures import get_location


@pytest.mark.asyncio
async def test_location_repository(container: Container):
    location_repository: BaseLocationRepository = container.resolve(
        BaseLocationRepository,
    )
    location_1: Location = next(get_location())
    await location_repository.add_location(location_1)

    assert await location_repository.get_location_by_name(location_1.name) == location_1

    location_2: Location = next(get_location())
    await location_repository.add_location(location_2)

    await location_repository.delete_location_by_name(location_1.name)

    with pytest.raises(LocationNotFoundException):
        await location_repository.get_location_by_name(location_1.name)

    await location_repository.delete_location_by_name(location_2.name)
