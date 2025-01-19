import asyncio

from aiogram import (
    Bot,
    Dispatcher,
)
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from faststream.rabbit import (
    RabbitBroker,
    RabbitQueue,
)

from infrastructure.message_broker.message import Message as BrokerMessage
from settings.config import config


broker = RabbitBroker(url="amqp://admin:admin@localhost:5672/")

bot: Bot = Bot(
    token=config.TELEGRAM_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)

dp = Dispatcher()


@dp.message(Command(commands=["start"]))
async def start_command(message: Message) -> None:
    user_id = message.from_user.id
    await message.reply(f"Ваш user_id: {user_id}")


@broker.subscriber(queue=RabbitQueue(name="user_queue", durable=True))
async def handle_user_notification(aio_message: dict) -> None:
    try:
        message: BrokerMessage = BrokerMessage(**aio_message)
        print(f"Получено сообщение: {message.data}")
        await bot.send_message(chat_id=688417643, text=message.data["login"])
    except Exception as e:
        print(f"Ошибка обработки сообщения: {e}")


async def main() -> None:
    await asyncio.gather(
        broker.start(),
        dp.start_polling(bot),
    )


if __name__ == "__main__":
    asyncio.run(main())
