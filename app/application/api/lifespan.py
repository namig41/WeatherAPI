from contextlib import asynccontextmanager

from fastapi import FastAPI

from aiosmtplib import SMTP
from infrastructure.database.models import (
    create_database,
    start_entity_mappers,
)
from infrastructure.email.init import connect_to_smtp_server
from punq import Container
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from application.di.container import init_container


@asynccontextmanager
async def lifespan(app: FastAPI):
    container: Container = init_container()

    engine: AsyncEngine = container.resolve(AsyncEngine)
    await create_database(engine)
    start_entity_mappers()

    smtp: SMTP = container.resolve(SMTP)
    await connect_to_smtp_server(smtp)

    yield
