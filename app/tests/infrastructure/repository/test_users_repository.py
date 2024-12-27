import pytest
from infrastructure.exceptions.repository import (
    UserExistsException,
    UserNotFoundException,
)
from infrastructure.repository.base import BaseUserRepository
from punq import Container

from domain.entities.user import User
from tests.fixtures import get_user


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

    with pytest.raises(UserExistsException):
        await users_repository.user_exists(user_2.login)
