from dataclasses import (
    dataclass,
    field,
)
from typing import Iterable

from infrastructure.exceptions.base import InfraException
from infrastructure.exceptions.repository import (
    LocationNotFoundException,
    UserNotFoundException,
)
from infrastructure.repository.base import BaseUserRepository

from domain.entities.location import Location
from domain.entities.user import User


@dataclass
class MemoryUserRepository(BaseUserRepository):

    _users: set[User] = field(
        default_factory=set,
    )

    async def add_user(self, user: User) -> None:
        self._users.add(user)

    async def get_user_by_login(self, login: str) -> User:
        try:
            return next(user for user in self._users if user.login == login)
        except StopIteration:
            raise UserNotFoundException()

    async def get_all_user(self) -> Iterable[User]:
        return self._users

    async def delete_user_by_login(self, login: str) -> None:
        try:
            user = await self.get_user_by_login(login)
            self._users.remove(user)
        except InfraException:
            raise

    def __len__(self) -> int:
        return len(self._users)


@dataclass
class MemoryLocationRepository(BaseUserRepository):

    _locations: set[User] = field(
        default_factory=set,
    )

    async def add_location(self, location: Location) -> None:
        self._locations.add(location)

    async def get_user_by_name(self, name: str) -> User:
        try:
            return next(
                location for location in self._locations if location.name == name
            )
        except StopIteration:
            raise LocationNotFoundException()

    async def get_all_location(self) -> Iterable[User]:
        return self._locations

    async def delete_location_by_name(self, name: str) -> None:
        try:
            location = await self.get_user_by_name(name)
            self._locations.remove(location)
        except InfraException:
            raise

    def __len__(self) -> int:
        return len(self._locations)
