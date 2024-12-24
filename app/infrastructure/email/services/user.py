from email.message import EmailMessage

from infrastructure.email.base import IEmailClientService
from infrastructure.email.config import ConfirmationEmailConfig

from domain.entities.user import User
from domain.exceptions.base import ApplicationException


async def send_user_registration_email(
    user: User,
    config: ConfirmationEmailConfig,
    email_service: IEmailClientService,
) -> None:
    try:
        message: EmailMessage = EmailMessage()

        message["From"] = config.email_from
        message["To"] = user.email.to_raw()
        message["Subject"] = config.subject

        message.set_content(
            f"Здравствуйте, {user.login}!\n\n"
            f"Благодарим вас за регистрацию на нашем сервисе. Ваш аккаунт был успешно создан.\n\n"
            f"Если у вас возникнут вопросы, пожалуйста, свяжитесь с нашей службой поддержки.\n\n"
            f"С уважением, команда {config.company_name}",
        )

        await email_service.send(message)
    except ApplicationException:
        raise


async def send_user_authorization_email(
    user: User,
    config: ConfirmationEmailConfig,
    email_service: IEmailClientService,
) -> None:
    try:
        message: EmailMessage = EmailMessage()

        message["From"] = config.email_from
        message["To"] = user.email.to_raw()
        message["Subject"] = config.subject

        message.set_content(
            f"Здравствуйте, {user.login}!\n\n"
            f"Мы зафиксировали вход в ваш аккаунт. Если это были вы, ничего делать не нужно.\n"
            f"Если вы не выполняли вход, рекомендуем немедленно \
            сменить пароль и связаться с нашей службой поддержки.\n\n"
            f"С уважением, команда {config.company_name}",
        )

        await email_service.send(message)
    except ApplicationException:
        raise
