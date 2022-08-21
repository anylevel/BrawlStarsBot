import asyncio

from app.models import Player
from app.sessions import Sessions
from app.handlers.brawl_api.utils import session_name_brawl_api


async def battle_log_update_info():
    while True:
        print(1)
        await asyncio.sleep(10)
