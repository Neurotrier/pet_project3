from aiogram import Router, types
from aiogram.filters.callback_data import CallbackData

from bot.parser import get_film

router = Router()


class FilmCallback(CallbackData, prefix="film"):
    ref: str


@router.callback_query(FilmCallback.filter())
async def cb_film(callback: types.CallbackQuery, callback_data: FilmCallback):
    film = await get_film({"ref": callback_data.ref})

    await callback.message.answer_photo(photo=film["image"],
                                        caption=f"Name: {film['name']}"
                                                f"\nYear: {film['year']}"
                                                f"\nLasting in min: {film['lasting']}"
                                                f"\nRating: {film['rating']}"
                                                f"\nRef: https://m.imdb.com{film['ref']}"
                                        )
    await callback.answer("Your film!")
