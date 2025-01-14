from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy.orm import registry

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
