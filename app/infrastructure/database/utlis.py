from sqlalchemy.ext.asyncio import AsyncEngine

from domain.entities.location import Location
from domain.entities.user import User
from infrastructure.database.models import (
    locations,
    mapper_registry,
    metadata,
    users,
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
