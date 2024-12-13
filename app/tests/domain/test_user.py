from faker import Faker

from domain.entities.user import User


def test_user_entity(faker: Faker) -> None:
    login: str = faker.name()
    password: str = faker.password()
    user: User = User(login, password)

    assert user.login == login
    assert user.password == password
