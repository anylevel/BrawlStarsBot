from aiogram.types import ContentType

from main import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from app.models import User
from app.handlers.brawl_api.utils import hashtag_check, hashtag_clan_check


class Token(StatesGroup):
    waiting_for_get_token = State()

    def __str__(self):
        return "TokenState"


class ClanToken(StatesGroup):
    waiting_for_get_token = State()
    finish_get_token = State()

    def __str__(self):
        return "ClanTokenState"


@dp.message_handler(commands=["start"], state="*")
async def start(message: types.Message, state: FSMContext):
    user = await User.get_or_none(name=message.from_user.username)
    if user:
        if user.token:
            await message.answer(f"Вы уже отправили токен боту,чтобы его поменять, воспользуйтесь командой /change")
            await message.answer_sticker(r"CAACAgIAAxkBAAEFi9xi9uvblI8N5D60sATRd5syM8FOzwAC9w4AAhLsuEm-DE44RkUN8CkE")
            await state.finish()
            return
    await message.answer(f"{message.from_user.username}, Введите токен")
    await Token.waiting_for_get_token.set()


@dp.message_handler(commands=["change"], state='*')
async def change(message: types.Message, state: FSMContext):
    user = await User.get_or_none(name=message.from_user.username)
    if user is None:
        await message.answer("Произошло что-то непредвиденное, пожалуйста запустите команду /start")
        await message.answer_sticker(r'CAACAgIAAxkBAAEFi9Zi9uuNW2iBg3Seg0Yri0hLTLoCPgAClxEAAgr0uUljGaSXWDc7hikE')
        await state.finish()
        return
    if user.token is None:
        await message.answer("Токен отсутствует, пожалуйста запустите команду /start")
        await message.answer_sticker(r'CAACAgIAAxkBAAEFi9hi9uuurzaZQ1xvvEMDWMd4nuSudQACdhAAAv1LuUlu4b2XAAHWXRUpBA')
        await state.finish()
        return
    await message.answer(f"{message.from_user.username}, Введите токен")
    await Token.waiting_for_get_token.set()


@dp.message_handler(commands=["cancel"], state="*")
async def cancel(message: types.Message, state: FSMContext):
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())
    await message.answer_sticker(r"CAACAgIAAxkBAAEFi9Bi9ur0VLRbIzRJQIBy60SLvhBj8AACXw8AAoljuEmgWDJHwB-2oCkE")
    await state.finish()


@dp.message_handler(state=Token.waiting_for_get_token)
async def finish_token(message: types.Message, state: FSMContext):
    token, result = await hashtag_check(message.text)
    if result is False:
        await message.reply(f"Токен {token} является некорректным.Пример: 9QCG9QC8C или 9qcg9qc8c\nВведите снова")
        return
    await User.update_or_create(name=message.from_user.username, defaults={"token": token})
    await state.finish()
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Да", "Нет"]
    keyboard.add(*buttons)
    await message.reply("Токен успешно обновлен!\nХотите добавить токен клана?", reply_markup=keyboard)
    await message.answer_sticker(r'CAACAgIAAxkBAAEFi8xi9uqzA053oQ7r8UdW6nUphYeT5wACcw4AAqoLuUnMpE9nFGaW9ykE')
    await ClanToken.next()


@dp.message_handler(state=ClanToken.waiting_for_get_token)
async def choose_clan_token(message: types.Message, state: FSMContext):
    if message.text == "Нет":
        await message.answer('Чтобы добавить токен клана,воспользуйтесь командой /change_clan',
                             reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
        return
    elif message.text == "Да":
        await message.answer('Введите токен клана', reply_markup=types.ReplyKeyboardRemove())
        await ClanToken.next()
        return
    else:
        await message.answer("Выберите один из ответов, нажав кнопку")


@dp.message_handler(state=ClanToken.finish_get_token)
async def finish_clan_token(message: types.Message, state: FSMContext):
    token, result = await hashtag_clan_check(hashtag=message.text)
    if result is False:
        await message.reply(f"Токен {token} является некорректным.Пример: 8YPQ209 или 8ypq209\nВведите снова!")
        return
    await User.update_or_create(name=message.from_user.username, defaults={"clan_token": token})
    await state.finish()
    await message.reply("Токен клана успешно обновлен!")
    await message.answer_sticker(r'CAACAgIAAxkBAAEFi8pi9uqPw9gi73z_7sZhjQoJ_J9yKAACiw8AAiRsuEkuUDkZ0De6TikE')


@dp.message_handler(content_types=ContentType.ANY)
async def action_without_command(message: types.Message):
    await message.answer("Я понимаю только команды которые придумал мой создатель!")
    await message.answer_sticker(r'CAACAgIAAxkBAAEFi9Ji9usSQiF5I18Ou98sZTK9wsdO2gACaBIAAnTBuEmtfv7mqk6xZikE')
