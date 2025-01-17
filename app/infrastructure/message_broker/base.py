from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass

from aio_pika.abc import AbstractChannel

from infrastructure.message_broker.message import Message


@dataclass
class BaseMessageBroker(ABC):
    channel: AbstractChannel

    @abstractmethod
    async def publish_message(
        self,
        message: Message,
        routing_key: str,
        exchange_name: str,
    ) -> None: ...

    @abstractmethod
    async def declare_exchange(self, exchange_name: str) -> None: ...

    async def set_channel(self, channel: AbstractChannel) -> None:
        self.channel = channel
