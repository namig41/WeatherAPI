from dataclasses import dataclass
from email.message import Message
from smtplib import SMTP
from typing import Any

from infrastructure.email.base import IEmailClientService


@dataclass
class SMTPEmailClient(IEmailClientService):
    client: SMTP

    def send(self, message: Message) -> Any:
        with self.client:
            self.client.send_message(message)
