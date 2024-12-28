from dataclasses import dataclass

import aioredis
from aioredis import Redis

from domain.entities.location import Location
from domain.entities.weather import Weather
from infrastructure.cache.base import ICacheWeatherService
from infrastructure.cache.config import CacheConfig
from infrastructure.cache.converters import (
    convert_weather_bytes_to_entity,
    convert_weather_entity_to_bytes,
)


@dataclass
class RedisCacheWeatherService(ICacheWeatherService):
    redis: Redis

    async def get_weather_by_location_name(self, location: Location) -> Weather | None:
        if weather_bytes := await self.redis.get(location.name):
            return convert_weather_bytes_to_entity(weather_bytes)
        return None

    async def set_weather_by_location_name(
        self,
        location: Location,
        weather: Weather,
        expire: int = 3600,
    ) -> None:
        weather_bytes: str = convert_weather_entity_to_bytes(weather)
        await self.redis.set(location.name, weather_bytes, expire)


def init_redis(cache_config: CacheConfig) -> Redis:
    return aioredis.from_url(cache_config.get_url("redis"))
