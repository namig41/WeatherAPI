from random import SystemRandom

import pytest
from faker import Faker
from punq import Container

from infrastructure.database.models import start_entity_mappers
from tests.fixtures import init_dummy_container


@pytest.fixture
def container() -> Container:
    return init_dummy_container()


@pytest.fixture(scope="session")
def faker() -> Faker:
    faker_instance: Faker = Faker()
    return faker_instance


@pytest.fixture(scope="session", autouse=True)
def setup_before_all_tests(faker: Faker) -> None:
    random_seed: int = SystemRandom().randint(0, 9999)
    faker.seed_instance(random_seed)

    start_entity_mappers()
