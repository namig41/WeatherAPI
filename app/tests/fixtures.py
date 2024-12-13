from typing import Generator

from faker import Faker
from punq import Container

from domain.entities.user import User
from infra.container.init import _init_container


def init_dummy_container() -> Container:
    container: Container = _init_container()
    return container


def get_user() -> Generator[User, None, None]:
    faker = Faker()

    while True:
        login: str = faker.name()
        password: str = faker.password()
        yield User(login, password)
