from fastapi import FastAPI
from fastapi.testclient import TestClient

import pytest

from bootstrap.di import init_container
from presentation.api.auth_service.v1.main import create_app as create_auth_service_app
from presentation.api.weather_service.v1.main import create_app as create_weather_service_app
from settings.config import config
from tests.fixtures import init_dummy_container


@pytest.fixture(scope="session")
def app_auth_service() -> FastAPI:
    app: FastAPI = create_auth_service_app()
    app.dependency_overrides[init_container] = init_dummy_container
    return app


@pytest.fixture(scope="session")
def app_weather_service() -> FastAPI:
    app: FastAPI = create_weather_service_app()
    app.dependency_overrides[init_container] = init_dummy_container
    return app


@pytest.fixture(scope="session")
def auth_client(app_auth_service: FastAPI) -> TestClient:
    return TestClient(app=app_auth_service)


@pytest.fixture(scope="session")
def weather_client(app_weather_service: FastAPI) -> TestClient:
    return TestClient(app=app_weather_service)


@pytest.fixture(scope="session")
def base_weather_service_url() -> str:
    return f"http://{config.WEATHER_SERIVCE_API_HOST}:{config.WEATHER_SERIVCE_API_PORT}"


@pytest.fixture(scope="session")
def base_auth_service_url() -> str:
    return f"http://{config.AUTH_SERIVCE_API_HOST}:{config.AUTH_SERIVCE_API_PORT}"


@pytest.fixture(scope="session")
def users_prefix() -> str:
    return "users"


@pytest.fixture(scope="session")
def auth_prefix() -> str:
    return "auth"


@pytest.fixture(scope="session")
def locations_prefix() -> str:
    return "locations"


@pytest.fixture(scope="function")
def test_user_data() -> dict:
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
