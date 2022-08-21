from aiogram import types
from main import dp
from app.sessions import Sessions
from .utils import get_token, get_clan_token, session_name_brawl_api, info_clan_members
from app.constans import brawlers_dict


@dp.message_handler(commands=["player_info"])
async def get_player_info(message: types.Message):
    token = await get_token(message=message)
    url_get_player_info = f"https://api.brawlstars.com/v1/players/%23{token}/"
    url_get_brawlers = "https://api.brawlstars.com/v1/brawlers"
    async with Sessions.get_response(name=session_name_brawl_api,
                                     url=url_get_player_info) as response_information_player, \
            Sessions.get_response(name=session_name_brawl_api, url=url_get_brawlers) as response_information_brawlers:
        brawlers = await response_information_brawlers.json()
        data = await response_information_player.json()
    top_brawlers = sorted(data['brawlers'], key=lambda item: item["trophies"], reverse=True)[:5]
    text_brawlers = ''
    for count, top_brawler in enumerate(top_brawlers, start=1):
        text_brawlers += f"  {count}.{top_brawler['name'].capitalize()}\n"
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
                         f"{text_brawlers}"
                         )
    await message.answer_sticker(brawlers_dict[top_brawlers[0]['name']])


@dp.message_handler(commands=["clan_info"])
async def get_clan_info(message: types.Message):
    clan_token = await get_clan_token(message=message)
    url_get_clan_info = f"https://api.brawlstars.com/v1/clubs/%23{clan_token}/"
    async with Sessions.get_response(name=session_name_brawl_api, url=url_get_clan_info) as response_clan_info:
        data = await response_clan_info.json()
    president, members_role = await info_clan_members(members=data["members"])
    top_players = data["members"][:5]
    await message.answer(f"Clan name:{data['name']}\n"
                         f"type:{data['type']}\n"
                         f"Required trophies:{data['requiredTrophies']}\n"
                         f"Trophies:{data['trophies']}\n"
                         f"Members:{len(data['members'])}/30\n"
                         f"President:\n"
                         f"     Name:{president['name']}\n"
                         f"     Tag:{president['tag']}\n"
                         f"     Trophies:{president['trophies']}\n"
                         f"Vice Presidents:{members_role['vicePresident']}\n"
                         f"Seniors:{members_role['senior']}\n"
                         f"Members:{members_role['member']}\n")
    await message.answer_sticker(r'CAACAgIAAxkBAAEFjJJi92Whb6i8h07EfMKTQGqJCAPpRgACdA4AAh7GUEviJXY_KNTeLykE')
    text_players = ''
    for count, top_player in enumerate(top_players, start=1):
        text_players += f"""
        {count}.Name:{top_player['name']}
                Tag:{top_player['tag']}
                Trophies:{top_player['trophies']}                        
                        """

    await message.answer(f"Top 5 players of the clan:\n"
                         f"{text_players}")

# TODO Сделать команду battlelog которая будет подсчитывать стату делать диаграммы и угарные смайлы типа мегахорош
# TODO  сделать рейтинг узнать код страны и сделать это все с обычной клавиатурой
