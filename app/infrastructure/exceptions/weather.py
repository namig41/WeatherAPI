from dataclasses import dataclass

from infrastructure.exceptions.base import InfraException


@dataclass(eq=False)
class WeatherAPIServiceException(InfraException):
    @property
    def message(self):
        return "Произошла ошибка при получении данных о погоде"
