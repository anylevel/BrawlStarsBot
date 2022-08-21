from main import dp, bot
from app.sessions import Sessions
from app.constans import brawlers_dict, sticker_trophies
from .utils import *
import random

session_name_brawlify = "brawlify"


@dp.message_handler(commands=['daily_meta'])
async def get_daily_meta(message: types.Message):
    url_get_events = "https://brawlify.com/#"
    async with Sessions.get_response(name=session_name_brawlify, url=url_get_events) as response_events:
        data_events = await response_events.read()
    buttons_current_events = await parse_daily_meta(data_events=data_events,
                                                    class_='container-fluid post-type4 pt-1 pb-3')
    keyboard_current_events = types.InlineKeyboardMarkup(row_width=1)
    keyboard_current_events.add(*buttons_current_events)
    await message.answer('Choose a mod to watch the win rate of brawlers:', reply_markup=keyboard_current_events)


@dp.message_handler(commands=['daily_meta_upcoming'])
async def get_daily_meta_upcoming(message: types.Message):
    url_get_events = "https://brawlify.com/#"
    async with Sessions.get_response(name=session_name_brawlify, url=url_get_events) as response_events:
        data_events = await response_events.read()
    buttons_upcoming_events = await parse_daily_meta(data_events=data_events, class_='container-fluid pb-2 post-type1')
    keyboard_upcoming_events = types.InlineKeyboardMarkup(row_width=1)
    keyboard_upcoming_events.add(*buttons_upcoming_events)
    await message.answer('Choose upcoming events to watch the win rate of brawler:',
                         reply_markup=keyboard_upcoming_events)


@dp.callback_query_handler(lambda c: "Win rate" in c.data)
async def choose_map(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    url_brawlify = "https://brawlify.com/#"
    brawl_map = callback_query.data.split(':')[1]
    async with Sessions.get_response(name=session_name_brawlify, url=url_brawlify) as response:
        data = await response.read()
    result_text, top_brawler = await parse_callback_win_rate(data=data, brawl_map=brawl_map)
    await bot.send_message(callback_query.from_user.id, result_text)
    await bot.send_sticker(callback_query.from_user.id, brawlers_dict[top_brawler])
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)


@dp.message_handler(commands=["best_teams"])
async def get_best_teams(message: types.Message):
    url_brawlify = "https://brawlify.com/#"
    async with Sessions.get_response(name=session_name_brawlify, url=url_brawlify) as response_events:
        data_events = await response_events.read()
    buttons = await parse_best_teams(data_events=data_events)
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await message.answer('Choose a mod to watch best teams brawlers on map:', reply_markup=keyboard)


@dp.callback_query_handler(lambda c: "Best teams" in c.data)
async def choose_map(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    url_brawlify = "https://brawlify.com/#"
    async with Sessions.get_response(name=session_name_brawlify, url=url_brawlify) as response:
        data = await response.read()
    result_text = await parse_callback_best_teams(data=data, callback_data=callback_query.data)
    sticker = random.choice(sticker_trophies)
    await bot.send_message(callback_query.from_user.id, result_text)
    await bot.send_sticker(callback_query.from_user.id, sticker)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
