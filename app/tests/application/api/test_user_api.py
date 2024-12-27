from fastapi.testclient import TestClient

import pytest
from httpx import Response


@pytest.mark.asyncio
async def test_api_add_user_request(
    test_user_data: dict,
    users_prefix: str,
    client: TestClient,
    base_url: str,
):

    response: Response = client.post(f"{base_url}/{users_prefix}", json=test_user_data)

    assert response.is_success


@pytest.mark.asyncio
async def test_api_get_users_request(
    users_prefix: str,
    client: TestClient,
    base_url: str,
):
    response: Response = client.get(f"{base_url}/{users_prefix}")
    assert response.is_success


@pytest.mark.asyncio
async def test_api_get_user_request(
    test_user_data: dict,
    users_prefix: str,
    client: TestClient,
    base_url: str,
):
    user_login: str = test_user_data["login"]
    response: Response = client.get(f"{base_url}/{users_prefix}/{user_login}")
    assert response.is_success
