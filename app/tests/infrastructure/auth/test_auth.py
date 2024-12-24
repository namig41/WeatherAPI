import pytest
from faker import Faker
from infrastructure.exceptions.auth import UserAuthFailedException
from infrastructure.repository.base import BaseUserRepository
from punq import Container

from domain.entities.user import User
from domain.interfaces.infrastructure.access_service import IAuthAccessService
from domain.interfaces.infrastructure.password_hasher import IPasswordHasher
from domain.value_objects.raw_password import RawPassword
from domain.value_objects.user_email import UserEmail


@pytest.mark.asyncio
async def test_authorize_service(faker: Faker, container: Container):
    access_service: IAuthAccessService = container.resolve(IAuthAccessService)
    password_hasher: IPasswordHasher = container.resolve(IPasswordHasher)
    users_repository: BaseUserRepository = container.resolve(BaseUserRepository)

    raw_password: RawPassword = RawPassword(faker.password())
    user: User = User.create_with_raw_password(
        faker.name_male(),
        UserEmail(faker.email()),
        raw_password,
        password_hasher,
    )
    await users_repository.add_user(user)

    await access_service.authorize(user.login, raw_password)

    fake_raw_password: RawPassword = RawPassword(faker.password())
    with pytest.raises(UserAuthFailedException):
        await access_service.authorize(user.login, fake_raw_password)
