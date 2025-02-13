from contextlib import asynccontextmanager

from fastapi import FastAPI

from infrastructure.database.utlis import start_entity_mappers


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_entity_mappers()
    yield
