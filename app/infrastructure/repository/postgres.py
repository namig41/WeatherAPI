from dataclasses import dataclass
from typing import Iterable

from sqlalchemy import (
    delete,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from domain.entities.location import Location
from domain.entities.user import User
from infrastructure.exceptions.repository import (
    LocationNotFoundException,
    UserExistsException,
    UserNotFoundException,
)
from infrastructure.repository.base import (
    BaseUserLocationRepository,
    BaseUserRepository,
)
from infrastructure.repository.filters import RepositoryFilters


@dataclass
class PostgreSQLUserRepository(BaseUserRepository):

    engine: AsyncEngine

    async def add_user(self, user: User) -> None:
        async with AsyncSession(self.engine, expire_on_commit=False) as session:
            session.add(user)
            await session.commit()

    async def user_exists(self, login: str) -> None:
        async with AsyncSession(self.engine, expire_on_commit=False) as session:
            query = select(User).where(User.login == login)
            result = await session.execute(query)
            if result.scalar_one_or_none() is not None:
                raise UserExistsException(login)

    async def get_user_by_login(self, login: str) -> User:
        async with AsyncSession(self.engine, expire_on_commit=False) as session:
            query = select(User).where(User.login == login)
            result = await session.execute(query)
            user: User | None = result.scalar_one_or_none()

            if not user:
                raise UserNotFoundException(login)

            return user

    async def get_all_user(self, filters: RepositoryFilters) -> Iterable[User]:
        async with AsyncSession(self.engine, expire_on_commit=False) as session:
            query = select(User).offset(filters.offset).limit(filters.limit)
            result = await session.scalars(query)
            users: Iterable[User] = result.all()
            return users

    async def delete_user_by_login(self, login: str) -> None:
        async with AsyncSession(self.engine, expire_on_commit=False) as session:
            query = delete(User).where(User.login == login)
            await session.execute(query)
            await session.commit()


@dataclass
class PostgreSQLUserLocationRepository(BaseUserLocationRepository):

    engine: AsyncEngine

    async def add_location(self, user: User, location: Location) -> None:
        async with AsyncSession(self.engine, expire_on_commit=False) as session:
            location.user_id = user.id
            session.add(location)
            await session.commit()

    async def get_location_by_name(self, user: User, name: str) -> Location:
        async with AsyncSession(self.engine, expire_on_commit=False) as session:
            query = select(Location).where(
                Location.name == name,
                Location.user_id == user.id,
            )
            result = await session.execute(query)
            location: Location | None = result.scalar_one_or_none()

            if not location:
                raise LocationNotFoundException()

            return location

    async def get_all_location(
        self, user: User, filters: RepositoryFilters,
    ) -> Iterable[Location]:
        async with AsyncSession(self.engine, expire_on_commit=False) as session:
            query = (
                select(Location)
                .where(Location.user_id == user.id)
                .offset(filters.offset)
                .limit(filters.limit)
            )
            result = await session.scalars(query)
            locations: Iterable[Location] = result.all()
            return locations

    async def delete_location_by_name(self, user: User, name: str) -> None:
        async with AsyncSession(self.engine, expire_on_commit=False) as session:
            query = delete(Location).where(
                Location.name == name,
                Location.user_id == user.id,
            )
            await session.execute(query)
            await session.commit()
