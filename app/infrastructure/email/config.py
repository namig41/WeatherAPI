from dataclasses import dataclass

from settings.config import config


@dataclass
class SMTPConfig:
    username: str = config.SMTP_USERNAME
    password: str = config.SMTP_PASSWORD
    port: int = config.SMTP_PORT
    host: str = config.SMTP_HOST
    use_tls: bool = True


@dataclass
class ConfirmationEmailConfig:
    email_from: str
    subject: str
    company_name: str
