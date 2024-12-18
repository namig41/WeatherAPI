from decimal import Decimal
from typing import Generator

from faker import Faker
from punq import Container

from application.di.container import _init_container
from domain.entities.location import Location
from domain.entities.user import User
from domain.value_objects.hashed_password import HashedPassword


def init_dummy_container() -> Container:
    container: Container = _init_container()
    return container


def get_user() -> Generator[User, None, None]:
    faker = Faker()

    while True:
        login: str = faker.name()
        password: str = faker.password()

        yield User(login, HashedPassword(password))


def get_location() -> Generator[Location, None, None]:
    faker = Faker()

    while True:
        login: str = faker.name()
        latitude: Decimal = faker.latitude()
        longitude: Decimal = faker.longitude()
        yield Location(login, latitude, longitude)
