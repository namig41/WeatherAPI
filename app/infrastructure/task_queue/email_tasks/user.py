import smtplib
from email.message import EmailMessage

from infrastructure.task_queue.init import celery_app
from settings.config import config


@celery_app.task
def send_user_confirmation_email(
    user_name: str,
    user_email: str,
) -> None:

    message: EmailMessage = EmailMessage()

    message["From"] = config.SMTP_USERNAME
    message["To"] = user_email
    message["Subject"] = "Добро пожаловать на наш сервис!"

    message.set_content(
        f"Здравствуйте, {user_name}!\n\n"
        f"Благодарим вас за регистрацию на нашем сервисе. Ваш аккаунт был успешно создан.\n\n"
        f"Если у вас возникнут вопросы, пожалуйста, свяжитесь с нашей службой поддержки.\n\n"
        f"С уважением, WeatherAPI",
    )

    with smtplib.SMTP_SSL(config.SMTP_HOST, config.SMTP_PORT) as server:
        server.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)
        server.send_message(message)
