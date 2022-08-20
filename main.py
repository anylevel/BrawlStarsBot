from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiohttp import ClientSession
from app.sessions import Sessions
from app.database import create_table, init
from app.middlewares import ThrottlingMiddleware, TokenMiddleware
from app.constans import get_token_bot, headers_brawl_api, headers_brawlify
import asyncio

bot = Bot(token=get_token_bot())
dp = Dispatcher(bot=bot, storage=MemoryStorage())


# TODO Разобраться в локалях языка и добавить их
# TODO Добавить логирование aiologger/logger/loguru?
# TODO добавить readme.md и в репу добавить пример config файла!


async def main():
    async with ClientSession(headers=headers_brawl_api) as session_brawl_api, ClientSession(
            headers=headers_brawlify) as session_brawlify:
        from app import dp
        Sessions(session=session_brawl_api, name="brawl_api")
        Sessions(session=session_brawlify, name="brawlify")
        await create_table()
        await init()

        dp.middleware.setup(ThrottlingMiddleware())
        dp.middleware.setup(TokenMiddleware())

        await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
