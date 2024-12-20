import pytest
from faker import Faker
from punq import Container

from domain.interfaces.infrastructure.password_hasher import IPasswordHasher
from domain.value_objects.hashed_password import HashedPassword
from domain.value_objects.raw_password import RawPassword


@pytest.mark.asyncio
async def test_authorize_service(faker: Faker, container: Container):
    password_hasher: IPasswordHasher = container.resolve(IPasswordHasher)

    raw_password: RawPassword = RawPassword(faker.password())
    hash_password: HashedPassword = password_hasher.hash_password(raw_password)

    assert password_hasher.verify_password(raw_password, hash_password)

    wrong_raw_password: RawPassword = RawPassword(faker.password())
    assert not password_hasher.verify_password(wrong_raw_password, hash_password)
