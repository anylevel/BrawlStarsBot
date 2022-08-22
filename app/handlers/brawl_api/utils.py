from app.sessions import Sessions
from app.models import User, Player, Club
from app.constans import sticker_win_rate
from aiogram import types
from typing import Any, Dict, List, Tuple
from collections import Counter, defaultdict

session_name_brawl_api = "brawl_api"


async def general_hashtag_check(hashtag: str) -> str:
    hashtag = hashtag.upper()
    if hashtag.startswith('#'):
        hashtag = hashtag[1:]
    return hashtag


async def hashtag_check(hashtag: str) -> tuple[str, bool, Any]:
    hashtag = await general_hashtag_check(hashtag=hashtag)
    url = f"https://api.brawlstars.com/v1/players/%23{hashtag}/"
    async with Sessions.get_response(name=session_name_brawl_api, url=url) as response:
        data = await response.json()
    if 'reason' in data:
        return hashtag, False, None
    return hashtag, True, data


async def hashtag_club_check(hashtag: str) -> tuple[str, bool, Any]:
    hashtag = await general_hashtag_check(hashtag=hashtag)
    url = f"https://api.brawlstars.com/v1/clubs/%23{hashtag}/"
    async with Sessions.get_response(name=session_name_brawl_api, url=url) as response:
        data = await response.json()
    if 'reason' in data:
        return hashtag, False, None
    return hashtag, True, data


async def get_token(message: types.Message):
    user = await User.get(name=message.from_user.username)
    return user.token


async def get_club_token(message: types.Message):
    user = await User.get(name=message.from_user.username)
    return user.club_token


async def get_player_from_user(message: types.Message):
    player = await Player.get(token=await get_token(message=message))
    return player


async def get_club_from_user(message: types.Message):
    clan = await Club.get(token=await get_club_token(message=message))
    return clan


async def info_club_members(members: List) -> Tuple[Dict, Dict]:
    members_role = Counter([member["role"] for member in members])
    for member in members:
        if member["role"] == "president":
            return member, members_role


async def stats_battle_showdown(battles: List[Dict], hashtag: str) -> tuple:
    hashtag = f"#{hashtag}"
    stats = {"wins": 0, "loses": 0, "draws": 0, "trophies": 0, "star_player_count": 0}
    brawlers = defaultdict(int)
    for battle in battles:
        stats, brawlers, result = await search_star_player(hashtag=hashtag, battle=battle, brawlers=brawlers,
                                                           stats=stats)
        if result:
            continue
        brawlers = await search_player(hashtag=hashtag, battle=battle, brawlers=brawlers)
        stats, result = await counter_battle_trio(battle=battle, stats=stats)
        if result:
            continue
        stats = await counter_battle_showdown(battle=battle, stats=stats)
    most_used_brawler = Counter(brawlers).most_common(1)
    return stats, most_used_brawler[0]


async def counter_battle_trio(battle: Dict, stats: Dict) -> tuple[Dict, bool]:
    flag = False
    if battle.get("trophyChange", 0):
        stats["trophies"] += battle["trophyChange"]
        if battle["trophyChange"] > 0:
            stats["wins"] += 1
        else:
            stats["loses"] += 1
        flag = True
    elif battle.get("result", 0):
        if battle["result"] == "victory":
            stats["wins"] += 1
        elif battle["result"] == "defeat":
            stats["loses"] += 1
        else:
            stats["draws"] += 1
        flag = True
    return stats, flag


async def counter_battle_showdown(battle: Dict, stats: Dict) -> Dict:
    rank = battle.get("rank", 0)
    if 'duo' in battle["mode"] and rank:
        if rank < 3:
            stats["wins"] += 1
        elif rank == 3:
            stats["draws"] += 1
        else:
            stats["loses"] += 1
    elif rank:
        if rank < 5:
            stats["wins"] += 1
        elif rank == 5:
            stats["draws"] += 1
        else:
            stats["loses"] += 1
    return stats


async def search_player(hashtag, battle: Dict, brawlers: Dict) -> Dict:
    battle_players = battle.get("players", 0)
    if battle_players:
        for battle_player in battle_players:
            if battle_player["tag"] == hashtag:
                brawlers[battle_player["brawler"]["name"]] += 1
                break
    else:
        for teams in battle["teams"]:
            flag = False
            for players in teams:
                if players["tag"] == hashtag:
                    brawlers[players["brawler"]["name"]] += 1
                    flag = True
                    break
            if flag:
                break
    return brawlers


async def search_star_player(hashtag: str, battle: Dict, brawlers: Dict, stats: Dict) -> tuple[dict, dict, bool]:
    star_player = battle.get("starPlayer", 0)
    flag = False
    if star_player:
        if star_player["tag"] == hashtag:
            brawlers[star_player["brawler"]["name"]] += 1
            stats["star_player_count"] += 1
            flag = True
    return stats, brawlers, flag


async def calculate_percent(stats: Dict, amount: int) -> tuple[int, int, int, str]:
    percent_wins = round(stats["wins"] / amount * 100, 3)
    percent_loses = round(stats["loses"] / amount * 100, 3)
    percent_draw = round(stats["draws"] / amount * 100, 3)
    sticker = ''
    if percent_wins > 75:
        sticker = sticker_win_rate["Best"]
    elif percent_wins > 65:
        sticker = sticker_win_rate["Good"]
    elif percent_wins > 55:
        sticker = sticker_win_rate["Good-middle"]
    elif percent_wins >= 40:
        sticker = sticker_win_rate["Middle"]
    elif percent_wins < 40:
        sticker = sticker_win_rate["Bad"]
    return percent_wins, percent_draw, percent_loses, sticker
