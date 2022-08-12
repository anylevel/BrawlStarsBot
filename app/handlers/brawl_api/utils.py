from app.sessions import Sessions
from app.models import User
from aiogram import types

session_name = "brawl_api"


async def hashtag_check(hashtag: str) -> tuple[str, bool]:
    hashtag = hashtag.upper()
    url = f"https://api.brawlstars.com/v1/players/%23{hashtag}/"
    async with Sessions.get_response(name=session_name, url=url) as response:
        data = await response.json()
    if 'reason' in data:
        return hashtag, False
    return hashtag, True


async def hashtag_clan_check(hashtag: str) -> tuple[str, bool]:
    hashtag = hashtag.upper()
    url = f"https://api.brawlstars.com/v1/clubs/%23{hashtag}/"
    async with Sessions.get_response(name=session_name, url=url) as response:
        data = await response.json()
    if 'reason' in data:
        return hashtag, False
    return hashtag, True


async def get_token(message: types.Message):
    user = await User.get(name=message.from_user.username)
    return user.token
