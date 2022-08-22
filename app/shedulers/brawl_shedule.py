from tortoise.models import Model
from typing import Optional, Callable, Coroutine, Dict, Type
from app.sessions import Sessions
from app.handlers.brawl_api.utils import session_name_brawl_api
import asyncio


async def brawl_schedule(time: int, model: Type[Model], func: Callable[[Dict, Optional[Model]], Coroutine],
                         url_model: str, endpoint: str = ''):
    while True:
        await asyncio.sleep(time)
        instances = await model.all()
        if not instances:
            continue
        for instance in instances:
            async with Sessions.get_response(name=session_name_brawl_api,
                                             url=f"https://api.brawlstars.com/v1/{url_model}/%23{instance.token}/{endpoint}") as response:
                data = await response.json()
            await func(data, instance)

# todo добавить команду в common типа об игроке будет выводить его токен  и токен клана типо вдруг он забудет
