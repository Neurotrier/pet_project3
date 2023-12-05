from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def get_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="/films 150")],
        [KeyboardButton(text="/series 150")],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard,
                               resize_keyboard=True,
                               input_field_placeholder="What to watch?")
