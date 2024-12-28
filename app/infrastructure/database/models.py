from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import registry

from domain.entities.location import Location
from domain.entities.user import User
from infrastructure.database.custom_types import (
    HashedPasswordType,
    UserEmailType,
)


mapper_registry = registry()
metadata = mapper_registry.metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("login", String(255), unique=True),
    Column("email", UserEmailType),
    Column("hashed_password", HashedPasswordType),
)

locations = Table(
    "locations",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), unique=True),
    Column("user_id", ForeignKey("users.id")),
    Column("latitude", Float),
    Column("longitude", Float),
)


def start_entity_mappers() -> None:
    mapper_registry.map_imperatively(User, users)
    mapper_registry.map_imperatively(Location, locations)


async def create_database(engine: AsyncEngine) -> None:
    async with engine.begin() as connection:
        await connection.run_sync(metadata.create_all)


async def drop_database(engine: AsyncEngine) -> None:
    async with engine.begin() as connection:
        await connection.run_sync(metadata.drop_all)
