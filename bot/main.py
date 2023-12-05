import asyncio
from aiogram import Bot, Dispatcher
from handlers import films, series, start
from callbacks import filmCallback, serieCallback
from config import TOKEN_API
from parser import *


async def on_startup():
    print("Alive!")


async def main():
    bot = Bot(TOKEN_API)
    dp = Dispatcher(bot=bot)
    dp.include_routers(films.router, series.router, start.router, filmCallback.router, serieCallback.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(on_startup())
    asyncio.run(main())
