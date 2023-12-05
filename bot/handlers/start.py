from aiogram import Router, types
from aiogram.filters import Command

from bot.keyboards.start_keyboard import get_keyboard

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        text=f"Hello, {message.from_user.username}!\n"
             "If you want to choose a movie or TV series, then you've come to the right place!\n"
             "The /films command (duration in minutes) will show all relevant films\n"
             "The command /series (number of episodes) will show all suitable series\n"
             "Try it!",
        reply_markup=await get_keyboard()

    )
