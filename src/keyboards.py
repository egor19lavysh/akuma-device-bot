from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import urllib
from src.photos import PHOTOS
from src.config import settings


def get_catalog_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for i in range(1, len(PHOTOS)):
        button = InlineKeyboardButton(
            text=PHOTOS[i]["name"],
            callback_data=f"device_{i}"
        )
        builder.add(button)

    builder.adjust(2)
    return builder.as_markup()

def interactive_keyboard(device_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    message_text = f"Привет! Я бы хотел(а) купить коврик {PHOTOS[device_id]['name']}"
    encoded_text = urllib.parse.quote(message_text)
    url = f"https://t.me/{settings.SELLER}?text={encoded_text}"

    button1 = InlineKeyboardButton(
        text="Перейти к заказу",
        url=url
    )
    button2 = InlineKeyboardButton(
        text="Назад",
        callback_data="back_to_catalog"
    )

    builder.row(button1)
    builder.row(button2)

    return builder.as_markup()

def get_back_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    back_button = InlineKeyboardButton(
        text="Назад",
        callback_data="back_to_catalog"
    )
    builder.add(back_button)

    return builder.as_markup()