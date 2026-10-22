from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
import urllib
from src.photos import PHOTOS
from src.config import settings


def get_catalog_keyboard(page: int = 1) -> InlineKeyboardMarkup:
    kb = []

    if page == 1:
        next_page_button = InlineKeyboardButton(text="Следующая страница ▶️", callback_data="next_page_2")
        
    else:
        next_page_button = InlineKeyboardButton(text="◀️ Назад", callback_data="next_page_1")

    kb.append([next_page_button])

    pages = {
        1: range(1, 13),
        2: range(13, 25)
    }

    buttons = []
    for i in pages.get(page):
        button = InlineKeyboardButton(
            text=PHOTOS[i]["name"],
            callback_data=f"device_{i}"
        )
        buttons.append(button)

    for idx in range(0, len(buttons), 2):
        row = buttons[idx:idx + 2]
        kb.append(row)

    ozon_button = InlineKeyboardButton(text="Ozon магазин", callback_data="to_ozon")
    kb.append([ozon_button])


    custom_button = InlineKeyboardButton(text="Custom Design", callback_data="custom_design")
    kb.append([custom_button])


    return InlineKeyboardMarkup(inline_keyboard=kb)

def interactive_keyboard(device_id: int, seller: str = settings.SELLER, device_name: str = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    device_name = device_name or PHOTOS[device_id]['name']
    message_text = f"Привет! Я бы хотел(а) купить коврик {device_name}"
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

def ozon_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Страница 1", url="https://www.ozon.ru/product/kovrik-dlya-myshki-bolshoy-dragonball-z-android-18-lazuli-5989371132/?sh=58l7zDhTWQ")],
        [InlineKeyboardButton(text="Страница 2", url="https://www.ozon.ru/product/kovrik-dlya-myshki-bolshoy-re-zero-emiliya-5989221022/?sh=58l7zDhTWQ")],
        [InlineKeyboardButton(text="Страница 3", url="https://www.ozon.ru/product/kovrik-dlya-myshki-bolshoy-evangelion-ayanami-rey-18-5989221163/?sh=58l7zDhTWQ")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_catalog")]
    ])