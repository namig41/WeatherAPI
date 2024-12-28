from dataclasses import dataclass
from email.message import Message
from typing import Any

from aiosmtplib import SMTP

from infrastructure.email.base import IEmailClientService


@dataclass
class AioSMTPEmailClient(IEmailClientService):
    client: SMTP

    async def send(self, message: Message) -> Any:
        async with self.client:
            await self.client.send_message(message)
