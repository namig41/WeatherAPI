from faker import Faker
from punq import Container

from domain.entities.user import User
from domain.interfaces.infrastructure.password_hasher import IPasswordHasher
from domain.value_objects.raw_password import RawPassword
from domain.value_objects.user_email import UserEmail


def test_user_entity(container: Container, faker: Faker) -> None:
    login: str = faker.name()
    email: UserEmail = UserEmail(faker.email())
    raw_password: RawPassword = RawPassword(faker.password())
    password_hasher: IPasswordHasher = container.resolve(IPasswordHasher)
    user: User = User.create_with_raw_password(
        login,
        email,
        raw_password,
        password_hasher,
    )

    assert user.login == login
    assert user.hashed_password == password_hasher.hash_password(raw_password)
