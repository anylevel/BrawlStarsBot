from app.sessions import Sessions
from app.models import User, Player, Clan
from aiogram import types
from typing import Any

session_name_brawl_api = "brawl_api"
session_name_brawlify = "brawlify"


async def hashtag_check(hashtag: str) -> tuple[str, bool, Any]:
    hashtag = hashtag.upper()
    url = f"https://api.brawlstars.com/v1/players/%23{hashtag}/"
    async with Sessions.get_response(name=session_name_brawl_api, url=url) as response:
        data = await response.json()
    if 'reason' in data:
        return hashtag, False, None
    return hashtag, True, data


# TODO сделать чтобы кушал хештег с решеткой
async def hashtag_clan_check(hashtag: str) -> tuple[str, bool, Any]:
    hashtag = hashtag.upper()
    url = f"https://api.brawlstars.com/v1/clubs/%23{hashtag}/"
    async with Sessions.get_response(name=session_name_brawl_api, url=url) as response:
        data = await response.json()
    if 'reason' in data:
        return hashtag, False, None
    return hashtag, True, data


async def get_token(message: types.Message):
    user = await User.get(name=message.from_user.username)
    return user.token


async def get_clan_token(message: types.Message):
    user = await User.get(name=message.from_user.username)
    return user.clan_token


async def get_player_from_user(message: types.Message):
    player = await Player.get(token=await get_token(message=message))
    return player


async def get_clan_from_user(message: types.Message):
    clan = await Clan.get(token=await get_clan_token(message=message))
    return clan
