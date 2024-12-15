from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass
class UserAuthFailedException(ApplicationException):
    @property
    def message(self):
        return "Ошибка авторизации"
