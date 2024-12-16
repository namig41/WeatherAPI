from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import (
    Any,
    TypeAlias,
)

from infrastructure.jwt.config import JWTConfig


JWTPayload: TypeAlias = dict[str, Any]
JWTToken: TypeAlias = str


@dataclass
class BaseJWTProcessor(ABC):
    jwt_config: JWTConfig

    @abstractmethod
    def encode(self, payload: JWTPayload) -> JWTToken: ...

    @abstractmethod
    def decode(self, token: JWTToken) -> JWTPayload: ...
