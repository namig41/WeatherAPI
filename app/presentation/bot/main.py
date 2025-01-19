import asyncio
import logging

from aiogram import (
    Bot,
    Dispatcher,
)

from presentation.bot.consumers.init import run_consumer
from presentation.bot.factory import get_telegram_bot
from presentation.bot.handlers.common_handler import router as common_handler


logging.basicConfig(level=logging.INFO)


async def run_bot() -> None:
    bot: Bot = get_telegram_bot()

    dp: Dispatcher = Dispatcher()

    dp.include_router(common_handler)

    await dp.start_polling(bot)


async def main() -> None:
    await asyncio.gather(
        run_bot(),
        run_consumer(),
    )


if __name__ == "__main__":
    asyncio.run(main())
