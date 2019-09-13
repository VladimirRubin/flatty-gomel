import logging
import settings

from aiogram import Bot, Dispatcher, executor, types

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    with open("users", "a") as f:
        f.write(str(f"{message.from_user.id}\n"))
    await message.reply("Привет, теперь я буду слать тебе варианты жилья по Гомелю!")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
