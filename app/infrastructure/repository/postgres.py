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
    Engine,
    select,
)
from sqlalchemy.orm import Session

from domain.entities.location import Location
from domain.entities.user import User


@dataclass
class PostgreSQLUserRepository(BaseUserRepository):

    engine: Engine

    async def add_user(self, user: User) -> None:
        with Session(self.engine) as session:
            session.add(user)
            session.commit()

    async def get_user_by_login(self, login: str) -> User:
        with Session(self.engine) as session:
            query = select(User).where(User.login == login)
            user: User | None = session.execute(query).scalar_one_or_none()

            if not user:
                raise UserNotFoundException()

            return user

    async def get_all_user(self) -> Iterable[User]:
        with Session(self.engine) as session:
            query = select(User)
            users: Iterable[User] = session.scalars(query).all()
            return users

    async def delete_user_by_login(self, login: str) -> None:
        with Session(self.engine) as session:
            query = delete(User).where(User.login == login)
            session.execute(query)
            session.commit()


@dataclass
class PostgreSQLLocationRepository(BaseLocationRepository):

    engine: Engine

    async def add_location(self, location: Location) -> None:
        with Session(self.engine) as session:
            session.add(location)
            session.commit()

    async def get_location_by_name(self, name: str) -> Location:
        with Session(self.engine) as session:
            query = select(Location).where(Location.name == name)
            location: Location | None = session.execute(query).scalar_one_or_none()

            if not location:
                raise LocationNotFoundException()

            return location

    async def get_all_location(self) -> Iterable[Location]:
        with Session(self.engine) as session:
            query = select(Location)
            locations: Iterable[Location] = session.scalars(query).all()
            return locations

    async def delete_location_by_name(self, name: str) -> None:
        with Session(self.engine) as session:
            query = delete(User).where(Location.name == name)
            session.execute(query)
            session.commit()
