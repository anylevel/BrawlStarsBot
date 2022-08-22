from typing import Optional
from app.models import Player

url_brawl_api = 'https://api.brawlstars.com/v1/players/'


async def change_battle_log(data: dict, player: Optional[Player]) -> None:
    if not player.battle_log or len(player.battle_log) >= 100:
        player.battle_log = data["items"]
        await player.save()
        return
    if player.battle_log == data["items"]:
        return
    new_items = [item for item in data["items"] if item not in player.battle_log]
    player.battle_log.extend(new_items)
    await player.save()
