from infrastructure.database.config import DBConfig
from infrastructure.exceptions.database import DatabaseRunFailedException
from sqlalchemy import (
    create_engine,
    Engine,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase


def init_database(db_config: DBConfig) -> Engine:
    engine = create_engine(
        db_config.database_url,
    )
    try:
        engine.connect()
    except SQLAlchemyError:
        raise DatabaseRunFailedException()
    return engine


class Base(DeclarativeBase):
    pass
