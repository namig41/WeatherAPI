from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class EmailNotValidException(ApplicationException):
    @property
    def message(self):
        return "Неверно введена почта пользователя"
