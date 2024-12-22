from dataclasses import dataclass

from email_validator import (
    EmailNotValidError,
    validate_email,
)

from domain.exceptions.user_email import EmailNotValidException
from domain.value_objects.base import BaseValueObject


@dataclass(frozen=True)
class UserEmail(BaseValueObject[str]):
    def validate(self) -> None:
        try:
            validate_email(self.value, check_deliverability=False)
        except EmailNotValidError:
            raise EmailNotValidException()
