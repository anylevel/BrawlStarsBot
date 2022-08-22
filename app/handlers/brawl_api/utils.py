from app.sessions import Sessions
from app.models import User, Player, Club
from aiogram import types
from typing import Any, Dict, List, Tuple
from collections import Counter

session_name_brawl_api = "brawl_api"


async def general_hashtag_check(hashtag: str) -> str:
    hashtag = hashtag.upper()
    if hashtag.startswith('#'):
        hashtag = hashtag[1:]
    return hashtag


async def hashtag_check(hashtag: str) -> tuple[str, bool, Any]:
    hashtag = await general_hashtag_check(hashtag=hashtag)
    url = f"https://api.brawlstars.com/v1/players/%23{hashtag}/"
    async with Sessions.get_response(name=session_name_brawl_api, url=url) as response:
        data = await response.json()
    if 'reason' in data:
        return hashtag, False, None
    return hashtag, True, data


async def hashtag_club_check(hashtag: str) -> tuple[str, bool, Any]:
    hashtag = await general_hashtag_check(hashtag=hashtag)
    url = f"https://api.brawlstars.com/v1/clubs/%23{hashtag}/"
    async with Sessions.get_response(name=session_name_brawl_api, url=url) as response:
        data = await response.json()
    if 'reason' in data:
        return hashtag, False, None
    return hashtag, True, data


async def get_token(message: types.Message):
    user = await User.get(name=message.from_user.username)
    return user.token


async def get_club_token(message: types.Message):
    user = await User.get(name=message.from_user.username)
    return user.club_token


async def get_player_from_user(message: types.Message):
    player = await Player.get(token=await get_token(message=message))
    return player


async def get_club_from_user(message: types.Message):
    clan = await Club.get(token=await get_club_token(message=message))
    return clan


async def info_club_members(members: List) -> Tuple[Dict, Dict]:
    members_role = Counter([member["role"] for member in members])
    for member in members:
        if member["role"] == "president":
            return member, members_role

