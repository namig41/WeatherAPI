from abc import abstractmethod
from email.message import Message
from typing import Protocol


class IEmailClientService(Protocol):
    @abstractmethod
    async def send(self, message: Message) -> None: ...
