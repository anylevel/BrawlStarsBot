from main import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from app.models import User
from app.handlers.brawl_api.utils import hashtag_check


# TODO Написать валидатор для хештега
# TODO разобраться с middleware


class Token(StatesGroup):
    waiting_for_get_token = State()

    def __str__(self):
        return "TokenState"


@dp.message_handler(commands=["start"], state="*")
async def start(message: types.Message, state: FSMContext):
    user = await User.get_or_none(name=message.from_user.username)
    if user:
        if user.token:
            await message.answer(f"Вы уже отправили токен боту,чтобы его поменять, воспользуйтесь командой /change")
            await state.finish()
            return
    await message.answer(f"{message.from_user.username}, Введите токен")
    await Token.waiting_for_get_token.set()


@dp.message_handler(commands=["change"], state='*')
async def change(message: types.Message, state: FSMContext):
    user = await User.get_or_none(name=message.from_user.username)
    if user is None:
        await message.answer("Произошло что-то непредвиденное, пожалуйста запустите команду /start")
        await state.finish()
        return
    if user.token is None:
        await message.answer("Токен отсутствует, пожалуйста запустите команду /start")
        await state.finish()
        return
    await message.answer(f"{message.from_user.username}, Введите токен")
    await Token.waiting_for_get_token.set()


@dp.message_handler(commands=["cancel"], state="*")
async def cancel(message: types.Message, state: FSMContext):
    await message.answer("Действие отменено")
    await state.finish()


@dp.message_handler(state=Token.waiting_for_get_token)
async def finish_token(message: types.Message, state: FSMContext):
    token, result = await hashtag_check(message.text)
    if result is False:
        await message.reply(f"Токен {token} является некорректным.Пример: 9QCG9QC8C или 9qcg9qc8c")
        return
    user = await User.get_or_none(name=message.from_user.username)
    if user is None:
        await User.create(name=message.from_user.username, token=message.text)
        await state.finish()
        return
    user.token = message.text
    await user.save()
    await state.finish()
    await message.reply("Токен успешно обновлен!")
