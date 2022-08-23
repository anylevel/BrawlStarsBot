from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiohttp import ClientSession
from app.sessions import Sessions
from app.database import create_table, init
from app.middlewares import ThrottlingMiddleware, TokenMiddleware
from app.constans import get_token_bot, headers_brawl_api, headers_brawlify
from app.models import Player, Club
from app.loggers import Loggers
import asyncio

bot = Bot(token=get_token_bot())
dp = Dispatcher(bot=bot, storage=MemoryStorage())


# TODO Разобраться в локалях языка и добавить их
# TODO добавить readme.md и в репу добавить пример config файла!


async def main():
    async with ClientSession(headers=headers_brawl_api) as session_brawl_api, ClientSession(
            headers=headers_brawlify) as session_brawlify:
        from app import dp
        from app.shedulers.brawl_shedule import brawl_schedule
        from app.shedulers.utils import change_battle_log, update_player, update_club
        Sessions(session=session_brawl_api, name="brawl_api")
        Sessions(session=session_brawlify, name="brawlify")
        await create_table()
        await init()
        logger = Loggers(filename='log_main.txt', name='log_main')
        dp.middleware.setup(ThrottlingMiddleware())
        dp.middleware.setup(TokenMiddleware())
        asyncio.create_task(
            brawl_schedule(time=10000, model=Player, func=change_battle_log, url_model='players', endpoint='battlelog'))
        asyncio.create_task(brawl_schedule(time=10000, model=Player, func=update_player, url_model='players'))
        asyncio.create_task(brawl_schedule(time=10000, model=Club, func=update_club, url_model='clubs'))
        await logger.info("Start polling")
        await dp.start_polling()


if __name__ == "__main__":
    asyncio.run(main())
