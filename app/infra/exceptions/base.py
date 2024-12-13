from domain.exceptions.base import ApplicationException


class InfraException(ApplicationException):
    @property
    def message(self):
        return "Ошибка на уровне инфраструктуры"
