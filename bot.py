"""
This is a echo bot.
It echoes any incoming text messages.
"""

import logging

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = "805817039:AAGeuzqxxJ0HjEL43f8TBtMmjl1Yo4oECRo"

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    with open("users", "a") as f:
        f.write(str(f"{message.from_user.id}\n"))
    await message.reply("Привет, теперь я буду слать тебе варианты жилья по Гомелю!")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
