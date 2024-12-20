from dataclasses import dataclass


@dataclass(frozen=True)
class WeatherAPIConfig:
    api_key: str
    base_url: str
