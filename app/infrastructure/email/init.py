from aiosmtplib import (
    SMTP,
    SMTPException,
)
from infrastructure.email.config import SMTPConfig
from infrastructure.exceptions.email_service import EmailConnectionFailedException


def init_smtp_client(smtp_config: SMTPConfig) -> SMTP:
    smtp: SMTP = SMTP(
        hostname=smtp_config.host,
        port=smtp_config.port,
        username=smtp_config.username,
        password=smtp_config.password,
        use_tls=smtp_config.use_tls,
    )
    return smtp


async def connect_to_smtp_server(smtp: SMTP) -> None:
    try:
        await smtp.connect()
    except SMTPException:
        raise EmailConnectionFailedException()
