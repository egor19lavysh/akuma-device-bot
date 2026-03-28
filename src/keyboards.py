from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import urllib
from src.photos import PHOTOS
from src.config import settings


def get_catalog_keyboard(page: int = 1) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    pages = {
        1: range(1, 13),
        2: range(13, 24)
    }

    for i in pages.get(page):
        button = InlineKeyboardButton(
            text=PHOTOS[i]["name"],
            callback_data=f"device_{i}"
        )
        builder.add(button)

    builder.adjust(2)

    ozon_button = InlineKeyboardButton(text="Ozon магазин", url="https://ozon.ru/t/p52tD2r")
    builder.row(ozon_button)

    if page == 1:
        next_page_button = InlineKeyboardButton(text="Следующая страница ▶️", callback_data="next_page_2")
        builder.row(next_page_button)
    else:
        next_page_button = InlineKeyboardButton(text="◀️ Назад", callback_data="next_page_1")
        builder.row(next_page_button)

    return builder.as_markup()

def interactive_keyboard(device_id: int, seller: str = settings.SELLER) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    message_text = f"Привет! Я бы хотел(а) купить коврик {PHOTOS[device_id]['name']}"
    encoded_text = urllib.parse.quote(message_text)
    url = f"https://t.me/{seller}?text={encoded_text}"

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