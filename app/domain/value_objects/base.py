from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import (
    Generic,
    TypeVar,
)


_T = TypeVar("_T")


@dataclass(frozen=True)
class BaseValueObject(ABC, Generic[_T]):

    value: _T

    def __post_init__(self):
        self.validate()

    @abstractmethod
    def validate(self) -> None: ...

    def as_type_value(self) -> _T:
        return self.value