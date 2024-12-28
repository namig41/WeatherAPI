from dataclasses import (
    dataclass,
    field,
)
from typing import Iterable

from domain.entities.location import Location
from domain.entities.user import User
from infrastructure.exceptions.base import InfraException
from infrastructure.exceptions.repository import (
    LocationNotFoundException,
    UserExistsException,
    UserNotFoundException,
)
from infrastructure.repository.base import (
    BaseLocationRepository,
    BaseUserRepository,
)


@dataclass
class MemoryUserRepository(BaseUserRepository):

    _users: set[User] = field(
        default_factory=set,
    )

    async def add_user(self, user: User) -> None:
        self._users.add(user)

    async def user_exists(self, login: str) -> bool:
        try:
            return bool(next(user for user in self._users if user.login == login))
        except StopIteration:
            raise UserExistsException(login)

    async def get_user_by_login(self, login: str) -> User:
        try:
            return next(user for user in self._users if user.login == login)
        except StopIteration:
            raise UserNotFoundException(login)

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
class MemoryLocationRepository(BaseLocationRepository):

    _locations: set[Location] = field(
        default_factory=set,
    )

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

    async def delete_location_by_name(self, name: str) -> None:
        try:
            location = await self.get_location_by_name(name)
            self._locations.remove(location)
        except InfraException:
            raise

    def __len__(self) -> int:
        return len(self._locations)
