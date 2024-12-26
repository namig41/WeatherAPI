from dataclasses import dataclass

from infrastructure.exceptions.base import InfraException


@dataclass(eq=False)
class EmailConnectionFailedException(InfraException):
    @property
    def message(self):
        return "Ошибка подключения к почте"


@dataclass(eq=False)
class EmailNotFoundException(InfraException):
    @property
    def message(self):
        return "Почта не найдена"
