from main import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from app.models import User
from app.middlewares import rate_limit

#TODO Написать валидатор для хештега, понять как доставать атрибуты из tortoise orm
#TODO разобраться с middleware


class Token(StatesGroup):
    waiting_for_get_token = State()


@dp.message_handler(commands=["start"], state="*")
@rate_limit(5,'start')
async def start(message: types.Message, state: FSMContext):
    user = await User.filter(name=message.from_user.username).first()
    if user:
        if user.token is not None:
            await message.answer(f"Вы уже отправили токен боту,чтобы его поменять, воспользуйтесь командой /change")
            await state.finish()
            return
    await message.answer(f"{message.from_user.username}, Введите токен")
    await Token.waiting_for_get_token.set()


@dp.message_handler(commands=["change"], state='*')
async def change(message: types.Message, state: FSMContext):
    user = await User.filter(name=message.from_user.username).first()
    if not user:
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
    print(message.text)
    user = User.filter(name=message.from_user.username).first()
    if not user:
        await User.create(name=message.from_user.username, token=message.text)
        return
    user.token = message.text
    await user.save()
    await state.finish()
