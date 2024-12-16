from dataclasses import dataclass

from infrastructure.exceptions.base import InfraException


@dataclass(eq=False)
class JWTDecodeException(InfraException):
    @property
    def message(self):
        return "Ошибка декодирования"


@dataclass(eq=False)
class JWTExpiredException(InfraException):
    @property
    def message(self):
        return "Ошибка декодирования"
