import json
from dataclasses import asdict

from domain.entities.weather import Weather


def convert_weather_entity_to_bytes(weather: Weather) -> str:
    return json.dumps(asdict(weather))


def convert_weather_bytes_to_entity(weather_bytes: str) -> Weather:
    return Weather(**json.loads(weather_bytes))
