from typing import List
from bs4 import BeautifulSoup
from aiogram import types

new_line = '\n'
new_line_f = '\\n'


async def parse_daily_meta(data_events: bytes) -> List:
    soup = BeautifulSoup(data_events, 'lxml')
    events = soup.find_all(class_='link opacity event-title-text event-title-map mb-0')
    buttons = list()
    for event in events:
        mode = event.find_previous().get('title')
        if 'Duo' in mode:
            continue
        brawl_map = event.get('title')
        buttons.append(
            types.InlineKeyboardButton(f"{mode}:{brawl_map}",
                                       callback_data=f"Win rate:{brawl_map}"))
    return buttons


async def parse_callback_win_rate(data: bytes, brawl_map: str) -> tuple[str, str]:
    soup = BeautifulSoup(data, 'lxml')
    brawlers = soup.find(class_='link opacity event-title-text event-title-map mb-0',
                         title=brawl_map).find_next().find_all('a')
    text_brawlers = f'Top players by winrate on map {brawl_map}:\n'
    top_brawler = brawlers[0].get('title').upper()
    for count, brawler in enumerate(brawlers, start=1):
        text_brawlers += f"{count}.{brawler.get('title').replace(new_line_f, ' ')}:{brawler.text.strip()}\n"
    return text_brawlers, top_brawler


async def parse_best_teams(data_events: bytes) -> List:
    buttons = list()
    soup = BeautifulSoup(data_events, 'lxml')
    all_events = soup.find_all(class_='link opacity event-title-text event-title-map mb-0')
    result_all_events = list()
    for event in all_events:
        mode = event.find_previous().get('title')
        brawl_map = event.get('title')
        result_all_events.append((mode, brawl_map))
    best_teams_events_data = soup.find_all('a', class_="link opacity h2")
    necessary_events = []
    for event in best_teams_events_data:
        necessary_events.append(event.text)
    for mode, brawl_map in result_all_events:
        if brawl_map in necessary_events and "Solo" not in mode:
            buttons.append(types.InlineKeyboardButton(f"{mode}:{brawl_map}",
                                                      callback_data=f"Best teams:{mode}:{brawl_map}"))
    return buttons


async def parse_callback_best_teams(data: bytes, callback_data: str):
    delimiter = 3
    _, brawl_mode, brawl_map = callback_data.split(':')
    if "Duo" in brawl_mode:
        delimiter = 2
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
    return text_brawlers
