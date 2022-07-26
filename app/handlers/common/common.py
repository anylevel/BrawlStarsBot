from aiogram.dispatcher.handler import CancelHandler
from aiogram.types import ContentType
from typing import Optional
from main import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from app.models import User, Player, Club
from app.handlers.brawl_api.utils import hashtag_check, hashtag_club_check


class Token(StatesGroup):
    waiting_for_get_token = State()

    def __str__(self):
        return "TokenState"


class ClubToken(StatesGroup):
    waiting_for_get_token = State()
    finish_get_token = State()

    def __str__(self):
        return "ClubTokenState"


@dp.message_handler(commands=["start"], state="*")
async def start(message: types.Message, state: FSMContext):
    user = await User.get_or_none(name=message.from_user.username)
    await state.finish()
    if user:
        if user.token:
            await message.answer(f"Вы уже отправили токен боту,чтобы его поменять, воспользуйтесь командой /change")
            await message.answer_sticker(r"CAACAgIAAxkBAAEFi9xi9uvblI8N5D60sATRd5syM8FOzwAC9w4AAhLsuEm-DE44RkUN8CkE")
            return
    await message.answer(f"{message.from_user.username}, Введите токен")
    await Token.waiting_for_get_token.set()


async def check_user(user: Optional[User], message: types.Message):
    if user is None:
        await message.answer("Произошло что-то непредвиденное, пожалуйста запустите команду /start")
        await message.answer_sticker(r'CAACAgIAAxkBAAEFi9Zi9uuNW2iBg3Seg0Yri0hLTLoCPgAClxEAAgr0uUljGaSXWDc7hikE')
        raise CancelHandler()


@dp.message_handler(commands=["change"], state='*')
async def change(message: types.Message, state: FSMContext):
    user = await User.get_or_none(name=message.from_user.username)
    await state.finish()
    await check_user(user=user, message=message)
    if user.token is None:
        await message.answer("Токен отсутствует, пожалуйста запустите команду /start")
        await message.answer_sticker(r'CAACAgIAAxkBAAEFi9hi9uuurzaZQ1xvvEMDWMd4nuSudQACdhAAAv1LuUlu4b2XAAHWXRUpBA')
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
    token, result, data = await hashtag_check(message.text)
    if result is False:
        await message.reply(
            f"Токен {token} является некорректным.Пример: 9QCG9QC8C , 9qcg9qc8c ,#9QCG9QC8C , #9qcg9qc8c \nВведите снова")
        return

    user, _ = await User.update_or_create(name=message.from_user.username, defaults={"token": token})
    player, _ = await Player.update_or_create(token=token,
                                              defaults={"name": data["name"], "trophies": data["trophies"],
                                                        "highest_trophies": data["highestTrophies"], "user": user})
    await state.finish()
    if user.club_token is None:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["Да", "Нет"]
        keyboard.add(*buttons)
        await message.reply("Токен успешно обновлен!\nХотите добавить токен клуба?", reply_markup=keyboard)
        await ClubToken.next()
        await message.answer_sticker(r'CAACAgIAAxkBAAEFi8xi9uqzA053oQ7r8UdW6nUphYeT5wACcw4AAqoLuUnMpE9nFGaW9ykE')
        return
    await message.reply("Токен успешно обновлен!")
    await message.answer_sticker(r'CAACAgIAAxkBAAEFi8xi9uqzA053oQ7r8UdW6nUphYeT5wACcw4AAqoLuUnMpE9nFGaW9ykE')


@dp.message_handler(commands=["add_club"], state='*')
async def add_club_token(message: types.Message, state: FSMContext):
    user = await User.get_or_none(name=message.from_user.username)
    await state.finish()
    await check_user(user=user, message=message)
    if user.club_token:
        await message.answer("Токен клуба есть, чтобы его поменять, воспользуйтесь командой /change_club")
        await message.answer_sticker(r'CAACAgIAAxkBAAEFi9hi9uuurzaZQ1xvvEMDWMd4nuSudQACdhAAAv1LuUlu4b2XAAHWXRUpBA')
        return
    await message.answer("Введите токен клуба:")
    await ClubToken.finish_get_token.set()


@dp.message_handler(commands=["change_club"], state="*")
async def change_club_token(message: types.Message, state: FSMContext):
    user = await User.get_or_none(name=message.from_user.username)
    await state.finish()
    await check_user(user=user, message=message)
    if user.club_token is None:
        await message.answer("Токен клуба отсутствует, чтобы его добавить, воспользуйтесь командой /add_club")
        await message.answer_sticker(r'CAACAgIAAxkBAAEFi9hi9uuurzaZQ1xvvEMDWMd4nuSudQACdhAAAv1LuUlu4b2XAAHWXRUpBA')
        return
    await message.answer("Введите токен клуба:")
    await ClubToken.finish_get_token.set()


@dp.message_handler(state=ClubToken.waiting_for_get_token)
async def choose_club_token(message: types.Message, state: FSMContext):
    if message.text == "Нет":
        await message.answer(
            'Чтобы добавить токен клуба потом,можно воспользоваться командой /add_club или /change_club если он есть',
            reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
        return
    elif message.text == "Да":
        await message.answer('Введите токен клуба:', reply_markup=types.ReplyKeyboardRemove())
        await ClubToken.next()
        return
    else:
        await message.answer("Выберите один из ответов, нажав кнопку")


@dp.message_handler(state=ClubToken.finish_get_token)
async def finish_club_token(message: types.Message, state: FSMContext):
    club_token, result, data = await hashtag_club_check(hashtag=message.text)
    if result is False:
        await message.reply(
            f"Токен {club_token} является некорректным.Пример: 8YPQ209 , 8ypq209 , #8YPQ209 ,#8ypq209 \nВведите снова!")
        return
    user, _ = await User.update_or_create(name=message.from_user.username,
                                          defaults={"club_token": club_token})
    club, _ = await Club.update_or_create(token=club_token,
                                          defaults={"name": data["name"], "trophies": data["trophies"], "user": user})

    await state.finish()
    await message.reply("Токен клуба успешно обновлен!")
    await message.answer_sticker(r'CAACAgIAAxkBAAEFi8pi9uqPw9gi73z_7sZhjQoJ_J9yKAACiw8AAiRsuEkuUDkZ0De6TikE')


@dp.message_handler(commands=['about'])
async def information_about_project(message: types.Message):
    buttons = [
        types.InlineKeyboardButton(text="Github", url='https://github.com/anylevel/BrawlStarsBot'),
        types.InlineKeyboardButton(text="Telegram", url='https://t.me/Anylevel')
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer("Information about the project and the author:", reply_markup=keyboard)
    await message.answer_sticker(r'CAACAgIAAxkBAAEFi95i9vY_P76wYjE3I3w6thQfjOUgIAACtwADw7nhMB8bl05QzRNTKQQ')


@dp.message_handler(commands=['current'])
async def current_condition(message: types.Message):
    user = await User.get_or_none(name=message.from_user.username)
    await check_user(user=user, message=message)
    if not user.token:
        user.token = 'Missing'
    if not user.club_token:
        user.club_token = 'Missing'
    await message.answer(f"Token player:{user.token}\nToken club:{user.club_token}")
    await message.answer_sticker(r'CAACAgIAAxkBAAEFpiVjBI15PXOBWSJhlh4e2lryWSGcCwAC2xcAAjbTkUhKz6LaFzZQPykE')


@dp.message_handler(content_types=ContentType.ANY)
async def action_without_command(message: types.Message):
    await message.answer("Я понимаю только команды которые придумал мой создатель!")
    await message.answer_sticker(r'CAACAgIAAxkBAAEFi9Ji9usSQiF5I18Ou98sZTK9wsdO2gACaBIAAnTBuEmtfv7mqk6xZikE')
