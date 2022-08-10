from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiohttp import ClientSession
from app.sessions import Sessions
from app.database import create_table, init
from app.middlewares import ThrottlingMiddleware, HandlerMiddleware
from app.constans import get_token
import asyncio
import os

BOT_TOKEN = os.getenv("API_TOKEN")
if not BOT_TOKEN:
    print("BOT_TOKEN is not found")
    exit(1)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())


async def main():
    headers = {
        "Accept": "application/json",
        "authorization": f"Bearer {await get_token()}"
    }
    async with ClientSession(headers=headers) as session:
        from app.handlers import dp, TokenMiddleware
        Sessions(session=session, name="brawl_api")
        await create_table()
        await init()
        dp.middleware.setup(HandlerMiddleware())
        dp.middleware.setup(TokenMiddleware())
        dp.middleware.setup(ThrottlingMiddleware())
        await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
