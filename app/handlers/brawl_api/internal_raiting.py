from aiogram import types
from app.models import Player, Club
from main import dp
from .utils import get_player_from_user, get_club_from_user
from app.constans import places, sticker_trophies, stickers_top_players, stickers_top_clubs
import random


@dp.message_handler(commands=["player_rating"])
async def internal_player_rating(message: types.Message):
    current_player = await get_player_from_user(message=message)
    players_count = await Player.all().count()
    players = await Player.all()
    top_players = players[:10]
    result_answer = 'Top 10 players:\n'
    for count, player in enumerate(top_players, start=1):
        result_answer += f'{count}.{player}\n'
    if current_player in top_players:
        place = top_players.index(current_player) + 1
        result_answer += f"Congratulations! You take the honorable {place}{places[str(place)]} place out of {players_count}"
        sticker = random.choice(stickers_top_players)
    else:
        place = players.index(current_player) + 1
        result_answer += f"Wow! You take the {place}{places[str(place)[-1]]} out of {players_count}"
        sticker = random.choice(sticker_trophies)
    await message.answer(result_answer)
    await message.answer_sticker(sticker)


@dp.message_handler(commands=["club_rating"])
async def internal_club_rating(message: types.Message):
    current_club = await get_club_from_user(message=message)
    clubs_count = await Club.all().count()
    clubs = await Club.all()
    top_clubs = clubs[:3]
    result_answer = 'Top 3 clubs:\n'
    for count, club in enumerate(top_clubs, start=1):
        result_answer += f'{count}.{club}\n'
    if current_club in top_clubs:
        place = top_clubs.index(current_club) + 1
        result_answer += f"Congratulations! Your club ranked {place}{places[str(place)]} place out of {clubs_count}"
        sticker = random.choice(stickers_top_clubs)
    else:
        place = clubs.index(current_club) + 1
        result_answer += f"Wow! Your club ranked {place}{places[str(place)[-1]]} out of {clubs_count}"
        sticker = random.choice(sticker_trophies)
    await message.answer(result_answer)
    await message.answer_sticker(sticker)
