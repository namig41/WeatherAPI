from abc import abstractmethod
from typing import Protocol

from .message import Message


class MessageBroker(Protocol):
    @abstractmethod
    async def publish_message(
        self,
        message: Message,
        routing_key: str,
        exchange_name: str,
    ) -> None: ...

    @abstractmethod
    async def declare_exchange(self, exchange_name: str) -> None: ...
