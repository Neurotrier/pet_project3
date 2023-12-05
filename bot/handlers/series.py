from aiogram import types, Router
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.callbacks.serieCallback import SerieCallback
from bot.parser import get_series

router = Router()


@router.message(Command("series"))
async def cmd_series(message: types.Message):
    if len(message.text.split(" ")) != 2:
        await message.reply("Your request should look like: /series 20 or /series 100")
    elif not message.text.split(" ")[1].isdigit():
        await message.reply("Episodes of the series is a positive number!")
    lasting = int(message.text.split(" ")[1])
    await message.answer(text="Please wait...")
    series = await get_series(lasting)
    keyboard = InlineKeyboardBuilder()
    for serie in series:
        keyboard.add(types.InlineKeyboardButton(
            text=f"{serie['name']}", callback_data=SerieCallback(
                ref=serie["ref"], lasting=int(serie["lasting"])).pack()
        ))
    keyboard.adjust(1)
    await message.answer(text="Chosen series", reply_markup=keyboard.as_markup())
