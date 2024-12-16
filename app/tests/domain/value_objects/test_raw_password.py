import re

import pytest

from domain.exceptions.raw_bassword import WeakPasswordException
from domain.value_objects.raw_password import RawPassword


def test_invalid_raw_password() -> None:
    invalid_passwords = {
        "": "Пароль должен состоять не менее из 8 символов",
        "short1@": "Пароль должен состоять не менее из 8 символов",
        "lowercase": "Пароль должен содержать заглавную букву.",
        "UPPERCASE": "Пароль не должен состоять только из заглавных букв.",
        "NoNumber!": "Пароль должен содержать число.",
        "NoSpecial8": "Пароль должен содержать в себе специальный             символ (@, #, $, %)",
        "With Space1!": "Пароль не должен содержать пробелы.",
    }

    for password, expected_message in invalid_passwords.items():
        with pytest.raises(WeakPasswordException, match=re.escape(expected_message)):
            RawPassword(password)
