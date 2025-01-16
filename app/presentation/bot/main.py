import asyncio

from aiogram import (
    Bot,
    Dispatcher,
)
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from faststream.rabbit import RabbitBroker

from settings.config import config


broker = RabbitBroker(url="amqp://admin:admin@rabbitmq:5672/")

bot: Bot = Bot(
    token=config.TELEGRAM_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)

dp = Dispatcher()


@dp.message(Command(commands=["start"]))
async def start_command(message: Message):
    user_id = message.from_user.id
    await message.reply(f"Ваш user_id: {user_id}")


@broker.subscriber("user.notifications")
async def handle_user_notification(message: dict):
    await bot.send_message(chat_id=688417643, text=message["message"])


async def main() -> None:
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
