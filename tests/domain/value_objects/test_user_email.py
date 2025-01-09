import pytest

from domain.exceptions.user_email import EmailNotValidException
from domain.value_objects.user_email import UserEmail


def test_invalid_user_email() -> None:
    with pytest.raises(EmailNotValidException):
        UserEmail("")
