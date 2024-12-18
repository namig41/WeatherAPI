from sqlalchemy import (
    Column,
    Engine,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy.orm import registry

from domain.entities.location import Location
from domain.entities.user import User


mapper_registry = registry()
metadata = mapper_registry.metadata

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("login", String(255)),
    Column("hashed_password", String(255)),
)

locations = Table(
    "locations",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255)),
    Column("user_id", ForeignKey("users.id")),
    Column("Latitude", Float),
    Column("Longitude", Float),
)


def start_mappers() -> None:
    mapper_registry.map_imperatively(
        User,
        users,
        properties={
            "id": users.c.id,
            "login": users.c.login,
            "hashed_password": users.c.hashed_password,
        },
    )
    mapper_registry.map_imperatively(Location, locations)


def create_database(engine: Engine) -> None:
    metadata.create_all(engine)
    start_mappers()
