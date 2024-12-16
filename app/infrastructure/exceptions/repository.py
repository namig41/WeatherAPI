from infrastructure.exceptions.base import InfraException


class UserNotFoundException(InfraException):
    @property
    def message(self):
        return "Пользователь не найден"


class LocationNotFoundException(InfraException):
    @property
    def message(self):
        return "Локация не найдена"
