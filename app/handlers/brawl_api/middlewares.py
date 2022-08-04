from app.models import User
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram import types


class TokenMiddleware(BaseMiddleware):
    def __init__(self):
        self.flag = False
        super(TokenMiddleware, self).__init__()

    async def on_pre_process_message(self, message: types.Message, data: dict):
        handler = current_handler.get()
        module_name = handler.__module__.split('.')[-1]
        if handler and module_name == "brawl_api":
            await self.check_token(message)

    async def check_token(self, message: types.Message):
        user = await User.filter(name=message.from_user.username).first()
        if not user:
            await message.answer("Произошло что-то непредвиденное, пожалуйста запустите команду /start")
            raise CancelHandler()
        elif user.token is None:
            await message.answer(f"Токен отсутствует, пожалуйста запустите команду /start")
            raise CancelHandler()
