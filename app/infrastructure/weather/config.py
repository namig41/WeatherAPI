from dataclasses import dataclass

from settings.config import config


@dataclass(frozen=True)
class WeatherAPIConfig:
    api_key: str = config.WEATHER_API_KEY
    base_url: str = config.WEATHER_API_URL
