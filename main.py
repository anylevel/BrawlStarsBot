from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiohttp import ClientSession
from app.sessions import Sessions
from app.database import create_table, init
from app.middlewares import *
from app.constans import get_token_api, get_token_bot
import asyncio

bot = Bot(token=get_token_bot())
dp = Dispatcher(bot=bot, storage=MemoryStorage())


async def main():
    headers = {
        "Accept": "application/json",
        "authorization": f"Bearer {await get_token_api()}"
    }
    async with ClientSession(headers=headers) as session:
        from app import dp
        Sessions(session=session, name="brawl_api")
        await create_table()
        await init()

        dp.middleware.setup(ThrottlingMiddleware())
        #dp.middleware.setup(HandlerMiddleware())
        dp.middleware.setup(TokenMiddleware())

        await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
