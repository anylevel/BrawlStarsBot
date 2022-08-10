import aiofiles


async def get_token() -> str:
    async with aiofiles.open("config.txt", 'r') as file:
        data = await file.read()
    token = data.rstrip()
    return token


commands = ["/start", "/change", "/cancel", "/player_info"]
states = ["Token:waiting_for_get_token"]
