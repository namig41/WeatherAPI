from email.message import EmailMessage

import pytest
from aiosmtplib import SMTP
from punq import Container

from infrastructure.email.config import SMTPConfig
from infrastructure.email.init import (
    connect_to_smtp_server,
    init_smtp_client,
)


@pytest.mark.asyncio
async def test_email_connection(container: Container):
    smtp_config: SMTPConfig = container.resolve(SMTPConfig)
    smtp: SMTP = init_smtp_client(smtp_config)

    await connect_to_smtp_server(smtp)

    message = EmailMessage()
    message["From"] = smtp_config.username
    message["To"] = smtp_config.username
    message["Subject"] = "Тестовое сообщение"
    message.set_content("Привет, это тестовое сообщение.")

    await smtp.send_message(message)

    await smtp.quit()
