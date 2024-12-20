import pytest
from infrastructure.exceptions.repository import (
    LocationNotFoundException,
    UserNotFoundException,
)
from infrastructure.repository.base import (
    BaseLocationRepository,
    BaseUserRepository,
)
from punq import Container

from domain.entities.location import Location
from domain.entities.user import User
from tests.fixtures import (
    get_location,
    get_user,
)


@pytest.mark.asyncio
async def test_users_repository(container: Container):
    users_repository: BaseUserRepository = container.resolve(BaseUserRepository)
    user_1: User = next(get_user())
    await users_repository.add_user(user_1)
    assert await users_repository.get_user_by_login(user_1.login) == user_1

    user_2: User = next(get_user())
    await users_repository.add_user(user_2)
    await users_repository.delete_user_by_login(user_1.login)

    with pytest.raises(UserNotFoundException):
        await users_repository.get_user_by_login(user_1.login)


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
