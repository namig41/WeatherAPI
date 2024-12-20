from dataclasses import dataclass

from domain.entities.base import BaseEntity


@dataclass
class Weather(BaseEntity):
    temperature: float
    description: str
    wind_speed: float
    humidity: int

    def validate(self) -> None: ...
