from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from src.photos import PHOTOS
from src.keyboards import get_catalog_keyboard, get_back_keyboard, interactive_keyboard


router = Router()

@router.message(Command("catalog"))
async def list_devices_handler(message: Message) -> None:
    await message.bot.send_photo(
        chat_id=message.chat.id,
        photo=PHOTOS[0]["file_id"],
        caption="Выберите коврик:",
        reply_markup=get_catalog_keyboard())
    
@router.callback_query(F.data.startswith("device_"))
async def device_callback_handler(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.delete()

    device_id = int(callback.data.split("_")[1])
    photo_info = PHOTOS.get(device_id)

    if photo_info:
        await callback.message.answer_photo(
            photo=photo_info["file_id"],
            caption=f"Вы выбрали коврик: {photo_info['name']}",
            reply_markup=interactive_keyboard(device_id=device_id)
        )
    else:
        await callback.message.answer("Извините, информация о выбранном коврике недоступна.", reply_markup=get_back_keyboard())

@router.callback_query(F.data == "back_to_catalog")
async def back_to_catalog_handler(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.delete()

    await callback.message.answer_photo(
        photo=PHOTOS[0]["file_id"],
        caption="Выберите коврик:",
        reply_markup=get_catalog_keyboard()
    )