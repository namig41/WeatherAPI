from fastapi import FastAPI
from fastapi.testclient import TestClient

import pytest
from presentation.api.main import create_app
from punq import Container

from application.di.container import init_container
from settings.config import Settings
from tests.fixtures import init_dummy_container


@pytest.fixture(scope="session")
def app() -> FastAPI:
    app: FastAPI = create_app()
    app.dependency_overrides[init_container] = init_dummy_container

    return app


@pytest.fixture(scope="session")
def client(app: FastAPI) -> TestClient:
    return TestClient(app=app)


@pytest.fixture(scope="session")
def base_url(container: Container) -> str:
    config: Settings = container.resolve(Settings)
    return f"http://{config.API_HOST}:{config.API_PORT}"


@pytest.fixture(scope="session")
def users_prefix() -> str:
    return "users"


@pytest.fixture(scope="session")
def locations_prefix() -> str:
    return "locations"


@pytest.fixture(scope="session")
def test_user_data(container: Container) -> dict:
    config: Settings = container.resolve(Settings)
    return {
        "login": "test",
        "email": config.SMTP_USERNAME,
        "password": "A1awq31das!@",
    }


@pytest.fixture(scope="session")
def test_location_data() -> dict:
    return {
        "name": "Moscow",
        "latitude": 55.75222,
        "longitude": 37.61556,
    }
