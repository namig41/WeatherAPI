import pytest
from punq import Container

from domain.entities.location import Location
from domain.entities.user import User
from infra.exceptions.repository import (
    LocationNotFoundException,
    UserNotFoundException,
)
from infra.repository.base import (
    BaseLocationRepository,
    BaseUserRepository,
)
from tests.fixtures import (
    get_location,
    get_user,
)


@pytest.mark.asyncio
async def test_memory_user_repository(container: Container):
    user_repository: BaseUserRepository = container.resolve(BaseUserRepository)
    user_1: User = next(get_user())
    await user_repository.add_user(user_1)

    assert await user_repository.get_user_by_login(user_1.login) == user_1

    user_2: User = next(get_user())
    await user_repository.add_user(user_2)

    assert len(user_repository) == 2

    await user_repository.delete_user_by_login(user_1.login)

    assert len(user_repository) == 1

    with pytest.raises(UserNotFoundException):
        await user_repository.get_user_by_login(user_1.login)


@pytest.mark.asyncio
async def test_memory_location_repository(container: Container):
    location_repository: BaseLocationRepository = container.resolve(
        BaseLocationRepository,
    )
    location_1: Location = next(get_location())
    await location_repository.add_location(location_1)

    assert await location_repository.get_location_by_name(location_1.name) == location_1

    location_2: Location = next(get_location())
    await location_repository.add_location(location_2)

    assert len(location_repository) == 2

    await location_repository.delete_location_by_name(location_1.name)

    assert len(location_repository) == 1

    with pytest.raises(LocationNotFoundException):
        await location_repository.get_location_by_name(location_1.name)
