from dataclasses import dataclass

from infrastructure.exceptions.base import InfraException


@dataclass(eq=False)
class PasswordMismatchException(InfraException):
    @property
    def message(self):
        return "Пароли не совпадают"


@dataclass(eq=False)
class UserAuthFailedException(InfraException):
    @property
    def message(self):
        return "Ошибка авторизации"
