from aiogram import Bot
from faststream.rabbit import (
    RabbitQueue,
    RabbitRouter,
)

from infrastructure.message_broker.message import Message as BrokerMessage
from presentation.bot.factory import get_telegram_bot
from presentation.bot.user import user


router = RabbitRouter()


@router.subscriber(queue=RabbitQueue(name="user_queue", durable=True))
async def handle_user_notification(aio_message: dict) -> None:
    try:
        message: BrokerMessage = BrokerMessage(**aio_message)
        bot: Bot = get_telegram_bot()
        user_login: str = message.data["login"]
        message_template: str = (
            f"Здравствуйте, {user_login}!\n\n"
            f"Благодарим вас за регистрацию на нашем сервисе. Ваш аккаунт был успешно создан.\n\n"
            f"Если у вас возникнут вопросы, пожалуйста, свяжитесь с нашей службой поддержки.\n\n"
            f"С уважением, WeatherAPI"
        )
        await bot.send_message(chat_id=user.id, text=message_template)
    except Exception as e:
        print(f"Ошибка обработки сообщения: {e}")
