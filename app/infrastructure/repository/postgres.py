from dataclasses import dataclass
from typing import Iterable

from infrastructure.exceptions.repository import (
    LocationNotFoundException,
    UserNotFoundException,
)
from infrastructure.repository.base import (
    BaseLocationRepository,
    BaseUserRepository,
)
from sqlalchemy import (
    delete,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from domain.entities.location import Location
from domain.entities.user import User


@dataclass
class PostgreSQLUserRepository(BaseUserRepository):

    engine: AsyncEngine

    async def add_user(self, user: User) -> None:
        async with AsyncSession(self.engine, expire_on_commit=False) as session:
            session.add(user)
            await session.commit()

    async def get_user_by_login(self, login: str) -> User:
        async with AsyncSession(self.engine, expire_on_commit=False) as session:
            query = select(User).where(User.login == login)
            result = await session.execute(query)
            user: User | None = result.scalar_one_or_none()

            if not user:
                raise UserNotFoundException()

            return user

    async def get_all_user(self) -> Iterable[User]:
        async with AsyncSession(self.engine, expire_on_commit=False) as session:
            query = select(User)
            result = await session.scalars(query)
            users: Iterable[User] = result.all()
            return users

    async def delete_user_by_login(self, login: str) -> None:
        async with AsyncSession(self.engine, expire_on_commit=False) as session:
            query = delete(User).where(User.login == login)
            await session.execute(query)
            await session.commit()


@dataclass
class PostgreSQLLocationRepository(BaseLocationRepository):

    engine: AsyncEngine

    async def add_location(self, location: Location) -> None:
        async with AsyncSession(self.engine, expire_on_commit=False) as session:
            session.add(location)
            await session.commit()

    async def get_location_by_name(self, name: str) -> Location:
        async with AsyncSession(self.engine, expire_on_commit=False) as session:
            query = select(Location).where(Location.name == name)
            result = await session.execute(query)
            location: Location | None = result.scalar_one_or_none()

            if not location:
                raise LocationNotFoundException()

            return location

    async def get_all_location(self) -> Iterable[Location]:
        async with AsyncSession(self.engine, expire_on_commit=False) as session:
            query = select(Location)
            result = await session.scalars(query)
            locations: Iterable[Location] = result.all()
            return locations

    async def delete_location_by_name(self, name: str) -> None:
        async with AsyncSession(self.engine, expire_on_commit=False) as session:
            query = delete(Location).where(Location.name == name)
            await session.execute(query)
            await session.commit()
