from fastapi.testclient import TestClient

import pytest
from httpx import Response


@pytest.mark.asyncio
async def test_api_add_location_request(
    test_location_data: dict,
    locations_prefix: str,
    client: TestClient,
    base_url: str,
):
    response: Response = client.post(
        f"{base_url}/{locations_prefix}",
        json=test_location_data,
    )

    assert response.is_success


@pytest.mark.asyncio
async def test_api_get_locations_request(
    locations_prefix: str,
    client: TestClient,
    base_url: str,
):
    response: Response = client.get(f"{base_url}/{locations_prefix}")
    assert response.is_success


@pytest.mark.asyncio
async def test_api_get_location_request(
    test_location_data: dict,
    locations_prefix: str,
    client: TestClient,
    base_url: str,
):
    location_name: str = test_location_data["name"]
    response: Response = client.get(f"{base_url}/{locations_prefix}/{location_name}")
    assert response.is_success
