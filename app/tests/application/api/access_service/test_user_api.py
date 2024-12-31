from fastapi.testclient import TestClient

import pytest
from httpx import Response


@pytest.mark.asyncio
async def test_api_add_user_request(
    test_user_data: dict,
    users_prefix: str,
    auth_client: TestClient,
    base_auth_service_url: str,
):
    response: Response = auth_client.post(
        f"{base_auth_service_url}/{users_prefix}",
        json=test_user_data,
    )

    assert response.is_success


@pytest.mark.asyncio
async def test_api_get_users_request(
    users_prefix: str,
    auth_client: TestClient,
    base_auth_service_url: str,
):
    response: Response = auth_client.get(f"{base_auth_service_url}/{users_prefix}")
    assert response.is_success


@pytest.mark.asyncio
async def test_api_get_user_request(
    test_user_data: dict,
    users_prefix: str,
    auth_client: TestClient,
    base_auth_service_url: str,
):
    user_login: str = test_user_data["login"]
    response: Response = auth_client.get(
        f"{base_auth_service_url}/{users_prefix}/{user_login}",
    )
    assert response.is_success
