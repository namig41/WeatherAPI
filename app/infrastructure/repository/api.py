from dataclasses import dataclass
from typing import Iterable

from httpx import (
    AsyncClient,
    HTTPStatusError,
    Response,
)
from infrastructure.repository.base import BaseUserRepository

from domain.entities.location import Location
from domain.entities.user import User


@dataclass
class APIUserRepository(BaseUserRepository):
    base_url: str

    async def add_user(self, user: User) -> None: ...

    async def get_user_by_login(self, login: str) -> User: ...

    async def get_all_user(self) -> Iterable[User]: ...

    async def delete_user_by_login(self, login: str) -> None: ...


@dataclass
class APILocationRepository(BaseUserRepository):
    base_url: str

    async def add_location(self, location: Location) -> None:
        async with AsyncClient() as client:
            try:
                response: Response = await client.post(
                    f"{self.base_url}/weather",
                    json=location,
                )
                response.raise_for_status()

            except HTTPStatusError:
                raise

    async def get_user_by_name(self, name: str) -> User:
        async with AsyncClient() as client:
            try:
                response: Response = await client.get(
                    f"{self.base_url}/weather",
                    params={
                        "name": name,
                    },
                )
                response.raise_for_status()
                return None
            except HTTPStatusError:
                raise

    async def get_all_location(self) -> Iterable[User]:
        return None

    async def delete_location_by_name(self, name: str) -> None: ...
