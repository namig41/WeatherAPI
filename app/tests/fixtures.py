from decimal import Decimal
from typing import Generator

from faker import Faker
from punq import Container

from bootstrap.di import _init_container
from domain.entities.location import Location
from domain.entities.user import User
from domain.value_objects.raw_password import RawPassword
from domain.value_objects.user_email import UserEmail
from infrastructure.auth.password_hasher import SHA256PasswordHasher


def init_dummy_container() -> Container:
    container: Container = _init_container()
    return container


def get_user() -> Generator[User, None, None]:
    faker: Faker = Faker()

    while True:
        login: str = faker.user_name()
        email: str = faker.email()
        password: str = faker.password(length=16)
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
