import aiofiles
import os


async def get_token_api() -> str:
    async with aiofiles.open("config.txt", 'r') as file:
        data = await file.read()
    token = data.rstrip()
    return token


def get_token_bot() -> str:
    bot_token = os.getenv("API_TOKEN")
    if not bot_token:
        raise ValueError("Ошибка при получении токена")
    return bot_token


#commands = ["/start", "/change", "/cancel", "/player_info"]
#states = ["Token:waiting_for_get_token", "ClanToken:waiting_for_get_token", "ClanToken:finish_get_token"]
