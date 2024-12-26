from fastapi.testclient import TestClient

import pytest
from httpx import Response


@pytest.mark.asyncio
async def test_api_add_user_request(
    client: TestClient,
    base_url: str,
):
    user_data: dict = {
        "login": "test",
        "email": "namigguseynov@yandex.ru",
        "password": "A1awq31das!@",
    }
    response: Response = client.post(f"{base_url}/users", json=user_data)

    assert response.is_success


@pytest.mark.asyncio
async def test_api_get_users_request(
    client: TestClient,
    base_url: str,
):
    response: Response = client.get(f"{base_url}/users")
    assert response.is_success


@pytest.mark.asyncio
async def test_api_get_user_request(
    client: TestClient,
    base_url: str,
):
    response: Response = client.get(f"{base_url}/users/test")
    assert response.is_success
