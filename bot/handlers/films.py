from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.callbacks.filmCallback import FilmCallback
from bot.parser import get_films

router = Router()


@router.message(Command("films"))
async def cmd_films(message: types.Message):
    if len(message.text.split(" ")) != 2:
        await message.reply("Your request should look like: /films 130 or /films 7")
    if not message.text.split(" ")[1].isdigit():
        await message.reply("Lasting of the films is a positive number!")
    lasting = int(message.text.split(" ")[1])
    await message.answer(text="Please wait...")
    films = await get_films(lasting)
    keyboard = InlineKeyboardBuilder()
    for film in films:
        keyboard.add(types.InlineKeyboardButton(
            text=f"{film['name']}", callback_data=FilmCallback(
                ref=film['ref']).pack()
        ))
    keyboard.adjust(1)
    await message.answer(text="Chosen films", reply_markup=keyboard.as_markup())
