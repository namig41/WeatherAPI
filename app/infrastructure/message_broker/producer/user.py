from infrastructure.message_broker.message import Message


async def send_user_notification(user_name: str) -> None:
    message: Message = Message(
        data=(
            f"Здравствуйте, {user_name}!\n\n"
            f"Благодарим вас за регистрацию на нашем сервисе. Ваш аккаунт был успешно создан.\n\n"
            f"Если у вас возникнут вопросы, пожалуйста, свяжитесь с нашей службой поддержки.\n\n"
            f"С уважением, WeatherAPI"
        ),
    )

    print(message.data)
