from decimal import Decimal

import pytest
from aioredis import Redis
from punq import Container

from domain.entities.location import Location
from domain.entities.weather import Weather
from infrastructure.cache.base import ICacheWeatherService
from infrastructure.cache.config import CacheConfig
from infrastructure.cache.redis import init_redis


@pytest.mark.asyncio
async def test_redis_connection():
    cache_config: CacheConfig = CacheConfig()
    redis: Redis = init_redis(cache_config)

    assert await redis.ping()


@pytest.mark.asyncio
async def test_cache_service(container: Container):
    location: Location = Location("Moscow", Decimal(55.751244), Decimal(37.618423))
    weather: Weather = Weather(37, "cloud", 30, 4)

    cache_service: ICacheWeatherService = container.resolve(ICacheWeatherService)

    await cache_service.set_weather_by_location_name(location, weather)
    await cache_service.get_weather_by_location_name(location) == weather
