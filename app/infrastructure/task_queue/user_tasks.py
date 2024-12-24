from email.message import EmailMessage

from infrastructure.email.base import IEmailClientService
from infrastructure.email.config import SMTPConfig
from infrastructure.email.converters import (
    convert_user_auth_to_email_message,
    convert_user_register_to_email_message,
)
from punq import Container

from application.di.container import init_container
from domain.entities.user import User
from domain.exceptions.base import ApplicationException


async def user_register_send_email_task(
    user: User,
    email_service: IEmailClientService,
) -> None:
    try:
        container: Container = init_container()
        smtp_config: SMTPConfig = container.resolve(SMTPConfig)
        user_register_message: EmailMessage = convert_user_register_to_email_message(
            user,
            smtp_config,
        )
        await email_service.send(user_register_message)
    except ApplicationException:
        raise


async def user_auth_send_email_task(
    user: User,
) -> None:
    try:
        container: Container = init_container()
        email_service: IEmailClientService = container.resolve(IEmailClientService)
        smtp_config: SMTPConfig = container.resolve(SMTPConfig)
        user_register_message: EmailMessage = convert_user_auth_to_email_message(
            user,
            smtp_config,
        )
        await email_service.send(user_register_message)
    except ApplicationException:
        raise
