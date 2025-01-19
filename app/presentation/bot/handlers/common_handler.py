from aiogram import (
    Router,
    types,
)
from aiogram.filters import (
    Command,
    CommandStart,
)

from presentation.bot.user import user


router = Router()


@router.message(CommandStart())
async def start_handler(message: types.Message):
    user.id = message.from_user.id
    await message.answer(
        "Привет! Я бот для приложения погоды. Используй /help, чтобы узнать доступные команды.",
    )


@router.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer(
        "/start - Приветствие\n",
    )
