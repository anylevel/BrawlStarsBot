from aiogram import Bot, Dispatcher
from aiohttp import ClientSession
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from app.database import create_table, init
import asyncio
import os
from tortoise import run_async

BOT_TOKEN = os.getenv("API_TOKEN")
if not BOT_TOKEN:
    print("BOT_TOKEN is not found")
    exit(1)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())

app_storage = {}


async def main():
    app_storage["session"] = ClientSession()
    async with app_storage["session"]:
        await create_table()
        await init()
        from app.handlers import dp
        await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
