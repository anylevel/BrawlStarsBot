from typing import Optional
from app.models import Player, Club

url_brawl_api = ''


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


async def update_player(data: dict, player: Optional[Player]) -> None:
    player = await player.update_from_dict(
        {"name": data["name"], "trophies": data["trophies"], "highest_trophies": data["highestTrophies"]})
    await player.save()


async def update_club(data: dict, club: Optional[Club]) -> None:
    club = await club.update_from_dict({"trophies": data["trophies"]})
    await club.save()
