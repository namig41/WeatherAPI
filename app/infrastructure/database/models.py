from typing import Any

from sqlalchemy import (
    Column,
    Dialect,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import registry
from sqlalchemy.types import TypeDecorator

from domain.entities.location import Location
from domain.entities.user import User
from domain.value_objects.hashed_password import HashedPassword


class HashedPasswordType(TypeDecorator):
    impl = String

    def process_bind_param(self, value: Any | None, dialect: Dialect) -> Any | None:
        if value is not None:
            return value.value
        return None

    def process_result_value(self, value: Any | None, dialect: Dialect) -> Any | None:
        if value is not None:
            return HashedPassword(value)
        return None

    def copy(self, **kwargs: Any) -> "HashedPasswordType":
        return self.__class__()


mapper_registry = registry()
metadata = mapper_registry.metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("login", String(255)),
    Column("hashed_password", HashedPasswordType),
)

locations = Table(
    "locations",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255)),
    Column("user_id", ForeignKey("users.id")),
    Column("latitude", Float),
    Column("longitude", Float),
)


def start_mappers() -> None:
    mapper_registry.map_imperatively(User, users)
    mapper_registry.map_imperatively(Location, locations)


async def create_database(engine: AsyncEngine) -> None:
    async with engine.begin() as connection:
        await connection.run_sync(metadata.create_all)
