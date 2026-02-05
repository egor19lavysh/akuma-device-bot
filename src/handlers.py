from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import Command
from src.photos import PHOTOS
from src.keyboards import get_catalog_keyboard, get_back_keyboard, interactive_keyboard
from aiogram.fsm.context import FSMContext


router = Router()

TEXT_DESC = """
Цена: {price}₽
Размер: 900х400мм
Толщина: 3мм
Покрытие: Speed/control

1. Противоскользящее резиновое основание
2. Аккуратно прошитые края
3. Подходит для ручной и бережной стирки в стиральной машине
"""

@router.message(Command("catalog"))
async def list_devices_handler(message: Message) -> None:
    await message.bot.send_photo(
        chat_id=message.chat.id,
        photo=PHOTOS[0]["file_id"],
        caption="Коврики доступны к <b>предзаказу</b>, а так же вы можете купить некоторые из них в нашем <b>магазине на Ozon</b>",
        parse_mode="HTML",
        reply_markup=get_catalog_keyboard())
    
@router.callback_query(F.data.startswith("device_"))
async def device_callback_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.delete()

    device_id = int(callback.data.split("_")[1])
    photo_info = PHOTOS.get(device_id)

    if photo_info:
        photo_ids = photo_info.get("ids", [])
        
        if photo_ids:
            media_group = [
                InputMediaPhoto(media=photo_id) 
                for photo_id in photo_ids
            ]
            # Добавляем подпись к последней фотографии
            media_group[-1].caption = f"<b>{photo_info['name']}</b>\n{TEXT_DESC.format(price=1900 if device_id <= 6 else 1700)}"
            media_group[-1].parse_mode = "HTML"
            
            msg_id = await callback.message.answer_media_group(media=media_group)
            await state.update_data(last_media_message_id=msg_id)
            await callback.message.answer(
                "Выберите действие:",
                reply_markup=interactive_keyboard(device_id=device_id)
            )
        else:
            await callback.message.answer("Извините, информация о выбранном коврике недоступна.", reply_markup=get_back_keyboard())
    else:
        await callback.message.answer("Извините, информация о выбранном коврике недоступна.", reply_markup=get_back_keyboard())

@router.callback_query(F.data == "back_to_catalog")
async def back_to_catalog_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    await callback.message.delete()

    # Удаляем последнее сообщение с медиа-группой
    last_message_id = (await state.get_data()).get("last_media_message_id")
    if last_message_id:
        for i in range(len(last_message_id)):
            await callback.message.bot.delete_message(
            chat_id=callback.message.chat.id,
            message_id=last_message_id[i].message_id
        )

    await callback.message.answer_photo(
        photo=PHOTOS[0]["file_id"],
        caption="Выберите коврик:",
        reply_markup=get_catalog_keyboard()
    )