from aiogram import Bot, Dispatcher
from aiohttp import ClientSession
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from app.database import create_table, init
from app.middlewares import ThrottlingMiddleware
import aiofiles
import asyncio
import os

BOT_TOKEN = os.getenv("API_TOKEN")
if not BOT_TOKEN:
    print("BOT_TOKEN is not found")
    exit(1)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())

app_storage = {}


async def main():
    async with aiofiles.open("./config.txt", 'r') as file:
        data = await file.read()
    token = data.rstrip()
    headers = {
        "Accept": "application/json",
        "authorization": f"Bearer {token}"
    }
    app_storage["session"] = ClientSession(headers=headers)
    async with app_storage["session"]:
        await create_table()
        await init()
        from app.handlers import dp , SomeMiddleware
        dp.middleware.setup(ThrottlingMiddleware())
        dp.middleware.setup(SomeMiddleware())
        await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
