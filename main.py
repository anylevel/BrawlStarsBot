from aiogram import Bot, Dispatcher, executor, types
from aiohttp import ClientSession
import aiosqlite
import asyncio
import os

BOT_TOKEN = os.getenv("API_TOKEN")
if not BOT_TOKEN:
    print("BOT_TOKEN is not found")
    exit(1)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot)

app_storage = {}


@dp.message_handler(commands=["start", "help"])
async def get_token(message: types.Message):
    await message.answer(f"kek_bek:{message.from_user.username}")


async def create_table() -> None:
    async with aiosqlite.connect("stats.db") as db:
        await db.execute(
            '''CREATE TABLE IF NOT EXISTS users (id integer primary key , user_name text , game_hashtag text)''')
        await db.commit()


async def main():
    app_storage["session"] = ClientSession()
    async with app_storage["session"]:
        await create_table()
        await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
