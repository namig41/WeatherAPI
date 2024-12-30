import pytest
from punq import Container

from domain.entities.location import Location
from domain.entities.user import User
from infrastructure.exceptions.repository import LocationNotFoundException
from infrastructure.repository.base import (
    BaseUserLocationRepository,
    BaseUserRepository,
)
from tests.fixtures import get_location


@pytest.mark.asyncio
async def test_location_repository(test_user_entity: User, container: Container):
    users_repository: BaseUserRepository = container.resolve(BaseUserRepository)

    await users_repository.add_user(test_user_entity)

    location_repository: BaseUserLocationRepository = container.resolve(
        BaseUserLocationRepository,
    )
    location_1: Location = next(get_location())
    await location_repository.add_location(test_user_entity, location_1)

    assert (
        await location_repository.get_location_by_name(
            test_user_entity, location_1.name,
        ) == location_1
    )

    location_2: Location = next(get_location())
    await location_repository.add_location(test_user_entity, location_2)

    await location_repository.delete_location_by_name(test_user_entity, location_1.name)

    with pytest.raises(LocationNotFoundException):
        await location_repository.get_location_by_name(
            test_user_entity, location_1.name,
        )

    await location_repository.delete_location_by_name(test_user_entity, location_2.name)

    await users_repository.delete_user_by_login(test_user_entity.login)
