from infrastructure.message_broker.config import EventBusConfig
from infrastructure.message_broker.init import init_message_broker
from infrastructure.message_broker.message import Message


broker = init_message_broker(EventBusConfig())


@broker.publisher("user.notifications")
async def send_user_notification(user_name: str) -> None:
    message: Message = Message(
        data=(
            f"Здравствуйте, {user_name}!\n\n"
            f"Благодарим вас за регистрацию на нашем сервисе. Ваш аккаунт был успешно создан.\n\n"
            f"Если у вас возникнут вопросы, пожалуйста, свяжитесь с нашей службой поддержки.\n\n"
            f"С уважением, WeatherAPI"
        ),
    )

    await broker.publish(message=message.to_json(), routing_key="user.notifications")
