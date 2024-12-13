import pytest
from punq import Container

from domain.entities.user import User
from infra.repository.base import BaseUserRepository
from tests.fixtures import get_user


@pytest.mark.asyncio
async def test_memory_user_repository(container: Container):
    user_repository: BaseUserRepository = container.resolve(BaseUserRepository)
    user: User = next(get_user())
    await user_repository.add_user(user)

    assert await user_repository.get_user_by_login(user.login) == user
