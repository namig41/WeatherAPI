from decimal import Decimal
from typing import Generator

from faker import Faker
from infrastructure.auth.password_hasher import SHA256PasswordHasher
from infrastructure.repository.base import (
    BaseLocationRepository,
    BaseUserRepository,
)
from infrastructure.repository.postgres import (
    PostgreSQLLocationRepository,
    PostgreSQLUserRepository,
)
from punq import (
    Container,
    Scope,
)

from application.di.container import _init_container
from domain.entities.location import Location
from domain.entities.user import User
from domain.value_objects.raw_password import RawPassword
from domain.value_objects.user_email import UserEmail


def init_dummy_container() -> Container:
    container: Container = _init_container()

    container.register(
        BaseUserRepository,
        PostgreSQLUserRepository,
        scope=Scope.singleton,
    )
    container.register(
        BaseLocationRepository,
        PostgreSQLLocationRepository,
        scope=Scope.singleton,
    )

    return container


def get_user() -> Generator[User, None, None]:
    faker: Faker = Faker()

    while True:
        login: str = faker.user_name()
        email: str = faker.email()
        password: str = faker.password()
        yield User.create_with_raw_password(
            login,
            UserEmail(email),
            RawPassword(password),
            SHA256PasswordHasher(),
        )


def get_location() -> Generator[Location, None, None]:
    faker: Faker = Faker()

    while True:
        location: str = faker.city()
        latitude: Decimal = faker.latitude()
        longitude: Decimal = faker.longitude()
        yield Location(location, latitude, longitude)
