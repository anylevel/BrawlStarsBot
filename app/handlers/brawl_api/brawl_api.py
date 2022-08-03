from app.models import User
from aiogram import types
from main import dp, app_storage


@dp.message_handler(commands=["player_info"])
async def get_player_info(message: types.Message):
    token = await get_token(message=message)
    url = f"https://api.brawlstars.com/v1/players/%23{token}/"
    async with app_storage["session"].get(url=url) as response:
        r = await response.json()
        await message.answer(r)


async def get_token(message: types.Message):
    user = User.filter(name=message.from_user.username).first()
    return user.token
