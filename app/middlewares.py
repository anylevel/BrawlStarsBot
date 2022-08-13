import asyncio
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled
from aiogram import types, Dispatcher
from .models import User


class ThrottlingMiddleware(BaseMiddleware):
    """
    Simple middleware
    """

    def __init__(self, limit=1, key_prefix='antiflood_message'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_pre_process_message(self, message: types.Message, data: dict):
        """
        This handler is called when dispatcher receives a message
        :param message:
        """
        # Get current handler
        handler = current_handler.get()

        # Get dispatcher from context
        dispatcher = Dispatcher.get_current()
        # If handler was configured, get rate limit and key from handler
        if handler:
            limit = self.rate_limit
            key = f"{self.prefix}_{handler.__name__}"
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"

        # Use Dispatcher.throttle method.
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            # Execute action
            await self.message_throttled(message, t, key)

            # Cancel current handler
            raise CancelHandler()

    async def message_throttled(self, message: types.Message, throttled: Throttled, key: str):
        """
        Notify user only on first exceed and notify about unlocking only on last exceed
        :param message:
        :param throttled:
        """
        dispatcher = Dispatcher.get_current()

        # Calculate how many time is left till the block ends
        # delta = throttled.rate - throttled.delta

        # Prevent flooding
        if throttled.exceeded_count <= 2:
            await message.reply('Too many requests! ')
            await message.answer_sticker(r'CAACAgIAAxkBAAEFi9Ri9utmtRVKxix9DPpTRQhjmyOapQACjBAAAj4iUUlZTqiYUcBoVCkE')

        # Sleep.
        await asyncio.sleep(10)

        # Check lock status
        thr = await dispatcher.check_key(key)

        # If current message is not last with current key - do not send message
        if thr.exceeded_count == throttled.exceeded_count:
            await message.reply('Unlocked.')


class TokenMiddleware(BaseMiddleware):
    def __init__(self):
        self.flag = False
        super(TokenMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        handler = current_handler.get()
        module_name = handler.__module__.split('.')[-1]
        if handler and module_name == "brawl_api":
            await self.check_token(message)

    async def check_token(self, message: types.Message):
        user = await User.get(name=message.from_user.username)
        if not user:
            await message.answer("Произошло что-то непредвиденное, пожалуйста запустите команду /start")
            raise CancelHandler()
        elif user.token is None:
            await message.answer(f"Токен отсутствует, пожалуйста запустите команду /start")
            raise CancelHandler()
