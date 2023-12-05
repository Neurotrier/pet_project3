from aiogram import types, Router
from aiogram.filters.callback_data import CallbackData

from bot.parser import get_serie

router = Router()


class SerieCallback(CallbackData, prefix="serie"):
    ref: str
    lasting: int


@router.callback_query(SerieCallback.filter())
async def cb_serie(callback: types.CallbackQuery, callback_data: SerieCallback):
    serie = await get_serie({"ref": callback_data.ref, "lasting": callback_data.lasting})
    await callback.message.answer_photo(photo=serie["image"],
                                        caption=f"Name: {serie['name']}"
                                                f"\nYear: {serie['year']}"
                                                f"\nEpisodes: {serie['lasting']}"
                                                f"\nRating: {serie['rating']}"
                                                f"\nRef: https://m.imdb.com{serie['ref']}"
                                        )
    await callback.answer("Your series!")
