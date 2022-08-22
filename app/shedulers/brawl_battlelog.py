from app.models import Player
from app.sessions import Sessions
from app.handlers.brawl_api.utils import session_name_brawl_api
from .utils import url_brawl_api, change_battle_log
import asyncio


async def battle_log_update_info():
    while True:
        # await asyncio.sleep(100)
        players = await Player.all()
        if not players:
            continue
        for player in players:
            async with Sessions.get_response(name=session_name_brawl_api,
                                             url=f"{url_brawl_api}%23{player.token}/battlelog") as response:
                data = await response.json()
            await change_battle_log(data=data, player=player)


# todo написать еще один планировщик который будет обновлять стату игроков
# todo добавить команду в common типа об игроке будет выводить его токен  и токен клана типо вдруг он забудет
