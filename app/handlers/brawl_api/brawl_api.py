from aiogram import types
from main import dp
from app.sessions import Sessions
from .utils import session_name, get_token
from app.constans import brawlers_dict


@dp.message_handler(commands=["player_info"])
async def get_player_info(message: types.Message):
    token = await get_token(message=message)
    url_get_player_info = f"https://api.brawlstars.com/v1/players/%23{token}/"
    url_get_brawlers = "https://api.brawlstars.com/v1/brawlers"
    async with Sessions.get_response(name=session_name, url=url_get_player_info) as response_information_player, \
            Sessions.get_response(name=session_name, url=url_get_brawlers) as response_information_brawlers:
        brawlers = await response_information_brawlers.json()
        data = await response_information_player.json()
        top_brawlers = sorted(data['brawlers'], key=lambda item: item["trophies"], reverse=True)[:5]
        await message.answer(f"Name:{data['name']}\n"
                             f"Trophies:{data['trophies']}\n"
                             f"Highest Trophies: {data['highestTrophies']}\n"
                             f"{len(data['brawlers'])}/{len(brawlers['items'])} Brawlers\n"
                             f"Victories:\n"
                             f"3vs3:{data['3vs3Victories']}\n"
                             f"solo:{data['soloVictories']}\n"
                             f"duo:{data['duoVictories']}\n"
                             f"Club: {data['club']['name']}\n\n"
                             f"Top 5 brawlers by trophies:\n"
                             f"  1.{top_brawlers[0]['name'].capitalize()}\n"
                             f"  2.{top_brawlers[1]['name'].capitalize()}\n"
                             f"  3.{top_brawlers[2]['name'].capitalize()}\n"
                             f"  4.{top_brawlers[3]['name'].capitalize()}\n"
                             f"  5.{top_brawlers[4]['name'].capitalize()}\n"
                             )
        await message.answer_sticker(brawlers_dict[top_brawlers[0]['name']])

# TODO кланы выводить название открыт/закрыт сколько трофеев нужно сколько всего трофеев
# TODO профиль президента сколько членов старейшин и т.д и топ 5 игроков
# @dp.message_handler(commands=[""])
