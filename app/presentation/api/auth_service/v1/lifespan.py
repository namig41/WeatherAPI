from contextlib import asynccontextmanager

from fastapi import FastAPI

from faststream.rabbit import RabbitBroker
from punq import Container
from sqlalchemy.ext.asyncio.engine import AsyncEngine

from bootstrap.di import init_container
from infrastructure.database.utlis import (
    create_database,
    start_entity_mappers,
)
from infrastructure.message_broker.config import EventBusConfig
from infrastructure.message_broker.init import init_message_broker


@asynccontextmanager
async def lifespan(app: FastAPI):
    container: Container = init_container()

    engine: AsyncEngine = container.resolve(AsyncEngine)
    await create_database(engine)
    start_entity_mappers()

    event_bus_config: EventBusConfig = container.resolve(EventBusConfig)
    broker: RabbitBroker = init_message_broker(event_bus_config)
    await broker.connect()
    yield
