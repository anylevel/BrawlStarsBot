from aiogram import types
from main import dp
from app.sessions import Sessions
from .utils import session_name, get_token


@dp.message_handler(commands=["player_info"])
async def get_player_info(message: types.Message):
    token = await get_token(message=message)
    url = f"https://api.brawlstars.com/v1/players/%23{token}/"
    async with Sessions.get_response(name=session_name, url=url) as response:
        r = await response.json()
        await message.answer(r)
