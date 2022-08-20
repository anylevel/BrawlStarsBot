from typing import Dict, List, Tuple
from aiogram import types
from main import dp, bot
from app.sessions import Sessions
from .utils import session_name_brawl_api, session_name_brawlify, get_token, get_clan_token
from app.constans import brawlers_dict, maps, sticker_trophies
from bs4 import BeautifulSoup
import random

new_line = '\n'
new_line_f = '\\n'


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


async def info_clan_members(members: List) -> Tuple[Dict, Dict]:
    president = dict()
    members_role = {"vicePresident": 0, "senior": 0, "member": 0}
    for member in members:
        if member["role"] == "president":
            president = member
        if member["role"] == "vicePresident":
            members_role["vicePresident"] += 1
        elif member["role"] == "senior":
            members_role["senior"] += 1
        elif member["role"] == "member":
            members_role["member"] += 1
    return president, members_role


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

#TODO сделать try except потому что словарь дырявый
#TODO разделить команды чтобы не просил токен!
@dp.message_handler(commands=['daily_meta'])
async def get_daily_meta(message: types.Message):
    url_get_events = 'https://api.brawlstars.com/v1/events/rotation'
    async with Sessions.get_response(name=session_name_brawl_api, url=url_get_events) as response_events:
        data_events = await response_events.json()
    buttons = list()
    for data_event in data_events:
        if 'duo' in data_event['event']['mode']:
            continue
        try:
            buttons.append(
                types.InlineKeyboardButton(f"{maps[data_event['event']['mode']]}:{data_event['event']['map']}",
                                           callback_data=f"Win rate:{data_event['event']['map']}"))
        except KeyError:
            await message.answer("К сожалению сервис сейчас недоступен!")
            return
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer('Choose a mod to watch the winrate of brawlers:', reply_markup=keyboard)


# TODO parse func
@dp.callback_query_handler(lambda c: "Win rate" in c.data)
async def choose_map(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    url_brawlify = "https://brawlify.com/#"
    brawl_map = callback_query.data.split(':')[1]
    async with Sessions.get_response(name=session_name_brawlify, url=url_brawlify) as response:
        data = await response.read()
    soup = BeautifulSoup(data, 'lxml')
    brawlers = soup.find(class_='link opacity event-title-text event-title-map mb-0',
                         title=brawl_map).find_next().find_all('a')
    text_brawlers = f'Top players by winrate on map {brawl_map}:\n'
    top_brawler = brawlers[0].get('title').upper()
    for count, brawler in enumerate(brawlers, start=1):
        text_brawlers += f"{count}.{brawler.get('title').replace(new_line_f, ' ')}:{brawler.text.strip()}\n"
    await bot.send_message(callback_query.from_user.id, text_brawlers)
    await bot.send_sticker(callback_query.from_user.id, brawlers_dict[top_brawler])
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)


@dp.message_handler(commands=["best_teams"])
async def get_best_teams(message: types.Message):
    url_get_events = 'https://api.brawlstars.com/v1/events/rotation'
    async with Sessions.get_response(name=session_name_brawl_api, url=url_get_events) as response_events:
        data_events = await response_events.json()
    buttons = list()
    for data_event in data_events:
        if 'solo' in data_event['event']['mode'] or 'big' in data_event['event']['mode']:
            continue
        mode = maps[data_event['event']['mode']]
        buttons.append(types.InlineKeyboardButton(f"{mode}:{data_event['event']['map']}",
                                                  callback_data=f"Best teams:{data_event['event']['map']}:{mode}"))
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer('Choose a mod to watch best teams brawlers on map:', reply_markup=keyboard)


# TODO func parse
@dp.callback_query_handler(lambda c: "Best teams" in c.data)
async def choose_map(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    delimiter = 3
    url_brawlify = "https://brawlify.com/#"
    _, brawl_map, brawl_mode = callback_query.data.split(':')
    if "Duo" in brawl_mode:
        delimiter = 2
    async with Sessions.get_response(name=session_name_brawlify, url=url_brawlify) as response:
        data = await response.read()
    soup = BeautifulSoup(data, 'lxml')
    info_maps = soup.find_all('a', class_="link opacity h2")
    result_map = ''
    for info_map in info_maps:
        if brawl_map in info_map.text:
            result_map = info_map
            break
    brawlers_data = result_map.find_next().find_next().find_all('img')
    brawlers = list()
    for brawler_data in brawlers_data:
        brawlers.append(brawler_data.get('title').replace(new_line_f, ' '))
    text_brawlers = f'The best teams on the map:{brawl_map}{new_line}'
    count = 1
    while brawlers:
        buffer = brawlers[:delimiter]
        brawlers = brawlers[delimiter:]
        text_brawlers += f"{str(count)}:{','.join(buffer)}{new_line}"
        count += 1
    sticker = random.choice(sticker_trophies)
    await bot.send_message(callback_query.from_user.id, text_brawlers)
    await bot.send_sticker(callback_query.from_user.id, sticker)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)

# TODO Сделать команду battlelog которая будет подсчитывать стату делать диаграммы и угарные смайлы типа мегахорош
# TODO  сделать рейтинг узнать код страны и сделать это все с обычной клавиатурой
