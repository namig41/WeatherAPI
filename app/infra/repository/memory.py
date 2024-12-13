from dataclasses import field
from typing import Iterable

from domain.entities.location import Location
from domain.entities.user import User
from infra.exceptions.repository import (
    LocationNotFoundException,
    UserNotFoundException,
)
from infra.repository.base import (
    BaseLocationRepository,
    BaseUserRepository,
)


class MemoryUserRepository(BaseUserRepository):

    _users: set[User] = field(default_factory=set)

    async def get_user_by_login(self, login: str) -> User:
        try:
            return next(user for user in self._users if user.login == login)
        except StopIteration:
            raise UserNotFoundException()

    async def get_all_user(self) -> Iterable[User]:
        return self._users

    async def delete_user_by_login(self, login: str) -> None:
        self._users.remove(User(login, ""))


class MemoryLocationRepository(BaseLocationRepository):

    _locations: set[Location] = field(default_factory=set)

    async def add_location(self, location: Location) -> None:
        self._locations.add(location)

    async def get_location_by_name(self, name: str) -> Location:
        try:
            return next(
                location for location in self._locations if location.name == name
            )
        except StopIteration:
            raise LocationNotFoundException()

    async def get_all_location(self) -> Iterable[Location]:
        return self._locations

    async def delete_location_by_name(self, name: str) -> None: ...
