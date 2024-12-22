from typing import Any

from sqlalchemy import (
    Dialect,
    String,
)
from sqlalchemy.types import TypeDecorator

from domain.value_objects.hashed_password import HashedPassword
from domain.value_objects.user_email import UserEmail


class HashedPasswordType(TypeDecorator):
    impl = String

    def process_bind_param(self, value: Any | None, dialect: Dialect) -> Any | None:
        if value is not None:
            return value.value
        return None

    def process_result_value(self, value: Any | None, dialect: Dialect) -> Any | None:
        if value is not None:
            return HashedPassword(value)
        return None

    def copy(self, **kwargs: Any) -> "HashedPasswordType":
        return self.__class__()


class UserEmailType(TypeDecorator):
    impl = String

    def process_bind_param(self, value: Any | None, dialect: Dialect) -> Any | None:
        if value is not None:
            return value.value
        return None

    def process_result_value(self, value: Any | None, dialect: Dialect) -> Any | None:
        if value is not None:
            return UserEmail(value)
        return None

    def copy(self, **kwargs: Any) -> "UserEmailType":
        return self.__class__()
