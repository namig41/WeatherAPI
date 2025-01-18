from contextlib import asynccontextmanager

from fastapi import FastAPI

from punq import Container
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from bootstrap.di import init_container
from infrastructure.database.utlis import (
    create_database,
    start_entity_mappers,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    container: Container = init_container()

    engine: AsyncEngine = container.resolve(AsyncEngine)
    await create_database(engine)
    start_entity_mappers()
    yield
