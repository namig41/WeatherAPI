from faker import Faker
from punq import Container

from domain.entities.user import User
from domain.interfaces.infrastructure.password_hasher import BasePasswordHasher
from domain.value_objects.raw_password import RawPassword


def test_user_entity(container: Container, faker: Faker) -> None:
    login: str = faker.name()
    raw_password: RawPassword = RawPassword(faker.password())
    password_hasher: BasePasswordHasher = container.resolve(BasePasswordHasher)
    user: User = User.create_with_raw_password(login, raw_password, password_hasher)

    assert user.login == login
    assert user.hashed_password == password_hasher.hash_password(raw_password)
