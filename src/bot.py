import asyncio
from os import getenv

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from src.config import settings
from src.handlers import router, list_devices_handler
import logging


logging.basicConfig(level=logging.INFO)

dp = Dispatcher()


# Command handler
@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.answer("Привет! Вот каталог наших ковриков:")
    await list_devices_handler(message)

@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    await message.answer("Чтобы посмотреть каталог ковриков, используйте команду /catalog")

@dp.message(F.photo)
async def command_photo_handler(message: Message) -> None:
    await message.answer(message.photo[-1].file_id)

# Run the bot
async def main() -> None:
    bot = Bot(token=settings.TOKEN)
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
          