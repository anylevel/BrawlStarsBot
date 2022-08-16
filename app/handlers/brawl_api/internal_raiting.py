from aiogram import types
from app.models import Player, Clan
from main import dp
from .utils import get_player_from_user, get_clan_from_user
from app.constans import places, sticker_trophies, stickers_top_players, stickers_top_clans
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


@dp.message_handler(commands=["clan_rating"])
async def internal_clan_rating(message: types.Message):
    current_clan = await get_clan_from_user(message=message)
    clans_count = await Clan.all().count()
    clans = await Clan.all()
    top_clans = clans[:3]
    result_answer = 'Top 3 clans:\n'
    for count, clan in enumerate(top_clans, start=1):
        result_answer += f'{count}.{clan}\n'
    if current_clan in top_clans:
        place = top_clans.index(current_clan) + 1
        result_answer += f"Congratulations! Your clan ranked {place}{places[str(place)]} place out of {clans_count}"
        sticker = random.choice(stickers_top_clans)
    else:
        place = clans.index(current_clan) + 1
        result_answer += f"Wow! Your clan ranked {place}{places[str(place)[-1]]} out of {clans_count}"
        sticker = random.choice(sticker_trophies)
    await message.answer(result_answer)
    await message.answer_sticker(sticker)
