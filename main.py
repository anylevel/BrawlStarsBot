from aiogram import Bot, Dispatcher, types
from aiohttp import ClientSession
from app.database import create_table
import asyncio
import os

BOT_TOKEN = os.getenv("API_TOKEN")
if not BOT_TOKEN:
    print("BOT_TOKEN is not found")
    exit(1)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot)

app_storage = {}


async def main():
    app_storage["session"] = ClientSession()
    async with app_storage["session"]:
        await create_table()
        await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
