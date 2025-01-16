from dataclasses import (
    asdict,
    dataclass,
    field,
)
from datetime import (
    datetime,
    timezone,
)
from uuid import UUID

import orjson
from uuid6 import uuid7


@dataclass(frozen=True, kw_only=True)
class Message:
    id: UUID = field(default_factory=uuid7)
    data: str = ""
    message_type: str = "message"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_json(self) -> str:
        return orjson.dumps(asdict(self), default=str).decode("utf-8")

    @classmethod
    def from_json(cls, json_str: str) -> "Message":
        data = orjson.loads(json_str)
        return cls(**data)
