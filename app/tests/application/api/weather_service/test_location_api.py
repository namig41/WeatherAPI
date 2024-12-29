from fastapi.testclient import TestClient

import pytest
from httpx import Response


@pytest.mark.asyncio
async def test_api_add_location_request(
    test_location_data: dict,
    locations_prefix: str,
    weather_client: TestClient,
    base_weather_service_url: str,
):
    response: Response = weather_client.post(
        f"{base_weather_service_url}/{locations_prefix}",
        json=test_location_data,
    )

    assert response.is_success


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
