from contextlib import asynccontextmanager
from smtplib import SMTP

from fastapi import FastAPI

from punq import Container
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from bootstrap.di import init_container
from infrastructure.database.models import (
    create_database,
    start_entity_mappers,
)
from infrastructure.email.init import connect_to_smtp_server


@asynccontextmanager
async def lifespan(app: FastAPI):
    container: Container = init_container()

    engine: AsyncEngine = container.resolve(AsyncEngine)
    await create_database(engine)
    start_entity_mappers()

    smtp: SMTP = container.resolve(SMTP)
    await connect_to_smtp_server(smtp)

    yield
