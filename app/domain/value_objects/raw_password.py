import re
from dataclasses import dataclass

from domain.exceptions.raw_bassword import WeakPasswordException
from domain.value_objects.base import BaseValueObject


MIN_PASSWORD_LENGHT = 8


def has_special_symbols(string: str) -> bool:
    regex = re.compile("[@_!#$%^&*()<>?/}{~:]")

    if re.search(regex, string) is None:
        return False

    return True


@dataclass(frozen=True)
class RawPassword(BaseValueObject[str]):

    def validate(self) -> None:
        error_messages = {
            "Пароль должен состоять не менее из 8 символов": lambda x: len(x)
            >= MIN_PASSWORD_LENGHT,  # noqa: W503
            "Пароль должен содержать заглавную букву.": lambda s: any(
                x.isupper() for x in s
            ),
            "Пароль не должен состоять только из заглавных букв.": lambda s: any(
                x.islower() for x in s
            ),
            "Пароль должен содержать число.": lambda s: any(x.isdigit() for x in s),
            "Пароль не должен содержать пробелы.": lambda s: not any(
                x.isspace() for x in s
            ),
            "Пароль должен содержать в себе специальный символ (@, #, $, %)": has_special_symbols,
        }

        for message, password_validator in error_messages.items():
            if not password_validator(self.value):
                raise WeakPasswordException(message)
