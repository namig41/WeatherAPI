from contextlib import asynccontextmanager

from fastapi import FastAPI

from infrastructure.database.models import (
    create_database,
    start_mappers,
)
from punq import Container
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from application.di.container import init_container


@asynccontextmanager
async def lifespan(app: FastAPI):
    container: Container = init_container()

    engine: AsyncEngine = container.resolve(AsyncEngine)
    await create_database(engine)
    start_mappers()

    yield
