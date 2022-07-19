from aiogram import Bot , Dispatcher , executor, types
from aiohttp import ClientSession
import os

BOT_TOKEN = os.getenv("API_TOKEN")
if not BOT_TOKEN:
    print("BOT_TOKEN is not found")
    exit(1)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=["start","help"])
async def get_token(message:types.Message):
    await message.reply("kek_bek")
    return 0


if __name__ == "__main__":
    executor.start_polling(dp,skip_updates=True)