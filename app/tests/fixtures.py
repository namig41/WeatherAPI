from decimal import Decimal
from functools import partial
from typing import Generator

from faker import Faker
from infrastructure.auth.password_hasher import SHA256PasswordHasher
from infrastructure.database.config import DBConfig
from infrastructure.database.init import init_database
from punq import (
    Container,
    Scope,
)
from sqlalchemy.ext.asyncio import AsyncEngine

from application.di.container import _init_container
from domain.entities.location import Location
from domain.entities.user import User
from domain.value_objects.raw_password import RawPassword
from domain.value_objects.user_email import UserEmail
from settings.config import Settings


def init_dummy_container() -> Container:
    container: Container = _init_container()
    config: Settings = container.resolve(Settings)

    db_config: DBConfig = DBConfig()
    db_config.DB_NAME = config.POSTGRES_TEST_DB

    container.register(
        AsyncEngine,
        factory=partial(init_database, db_config=db_config),
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
