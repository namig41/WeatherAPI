from dataclasses import dataclass

from infrastructure.exceptions.base import InfraException


@dataclass(eq=False)
class UserNotFoundException(InfraException):
    login: str

    @property
    def message(self):
        return f"Пользователь {self.login} не найден"


@dataclass(eq=False)
class UserExistsException(InfraException):
    login: str

    @property
    def message(self):
        return f"Пользователь с таким именем {self.login} существует"


@dataclass(eq=False)
class LocationNotFoundException(InfraException):
    @property
    def message(self):
        return "Локация не найдена"


@dataclass(eq=False)
class LocationExistsException(InfraException):
    @property
    def message(self):
        return "Локация существует"
