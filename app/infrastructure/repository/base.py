from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import Iterable

from domain.entities.location import Location
from domain.entities.user import User
from infrastructure.repository.filters import RepositoryFilters


@dataclass
class BaseUserRepository(ABC):

    @abstractmethod
    async def add_user(self, user: User) -> None: ...

    @abstractmethod
    async def user_exists(self, login: str) -> None: ...

    @abstractmethod
    async def get_user_by_login(self, login: str) -> User: ...

    @abstractmethod
    async def get_all_user(self, filters: RepositoryFilters) -> Iterable[User]: ...

    @abstractmethod
    async def delete_user_by_login(self, login: str) -> None: ...


@dataclass
class BaseUserLocationRepository(ABC):

    @abstractmethod
    async def add_location(self, user: User, location: Location) -> None: ...

    @abstractmethod
    async def get_location_by_name(self, user: User, name: str) -> Location: ...

    @abstractmethod
    async def get_all_location(
        self, user: User, filters: RepositoryFilters,
    ) -> Iterable[Location]: ...

    @abstractmethod
    async def delete_location_by_name(self, user: User, name: str) -> None: ...
