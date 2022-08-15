from aiogram import types
from app.models import Player
from main import dp
from .utils import get_player_from_user
from app.constans import places, sticker_trophies, stickers_top_players
import random


@dp.message_handler(commands=["player_rating"])
async def internal_player_rating(message: types.Message):
    current_player = await get_player_from_user(message=message)
    players_count = await Player.all().count()
    players = await Player.all()
    top_players = players[:3]
    text = ''
    for count, player in enumerate(top_players, start=1):
        text += f'{count}.{player}\n'
    if current_player in top_players:
        place = top_players.index(current_player) + 1
        text += f"Congratulations! you take the honorable {place}{places[str(place)]} place out of {players_count}"
        sticker = random.choice(stickers_top_players)
    else:
        place = players.index(current_player) + 1
        text += f"Wow! You take the {place}{places[str(place)[-1]]} out of {players_count}"
        sticker = random.choice(sticker_trophies)
    await message.answer(text)
    await message.answer_sticker(sticker)
