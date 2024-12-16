from dataclasses import dataclass

from domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class WeakPasswordException(ApplicationException):
    error_message: str

    @property
    def message(self):
        return self.error_message
