from fastapi.testclient import TestClient

import pytest
from httpx import Response


@pytest.mark.asyncio
async def test_api_add_location_request(
    test_location_data: dict,
    locations_prefix: str,
    auth_prefix: str,
    users_prefix: str,
    base_weather_service_url: str,
    base_auth_service_url: str,
    test_user_data: dict,
    auth_client: TestClient,
    weather_client: TestClient,
):
    add_user_response: Response = auth_client.post(
        f"{base_auth_service_url}/{users_prefix}",
        json=test_user_data,
    )

    assert add_user_response.status_code == 201

    auth_response: Response = auth_client.post(
        f"{base_auth_service_url}/{auth_prefix}/login",
        data={
            "username": test_user_data["login"],
            "password": test_user_data["password"],
        },
    )
    assert auth_response.status_code == 200
    token: str = auth_response.json().get("access_token")
    assert token is not None

    headers: dict = {"Authorization": f"Bearer {token}"}
    location_add_response = weather_client.post(
        f"{base_weather_service_url}/{locations_prefix}",
        json=test_location_data,
        headers=headers,
    )

    assert location_add_response.status_code == 200
    assert location_add_response.json()["status"] == "success"


@pytest.mark.asyncio
async def test_api_get_locations_request(
    locations_prefix: str,
    weather_client: TestClient,
    base_weather_service_url: str,
):
    response: Response = weather_client.get(
        f"{base_weather_service_url}/{locations_prefix}",
    )
    assert response.is_success


@pytest.mark.asyncio
async def test_api_get_location_request(
    test_location_data: dict,
    locations_prefix: str,
    weather_client: TestClient,
    base_weather_service_url: str,
):
    location_name: str = test_location_data["name"]
    response: Response = weather_client.get(
        f"{base_weather_service_url}/{locations_prefix}/{location_name}",
    )
    assert response.is_success
