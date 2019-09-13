import asyncio
import ujson
import logging
from string import Template

import templates

from aiogram import Bot, Dispatcher, types
from aiogram.utils import exceptions, executor

from utils import get_rent_type

API_TOKEN = "805817039:AAGeuzqxxJ0HjEL43f8TBtMmjl1Yo4oECRo"

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("broadcast")

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


def get_users():
    users = []
    with open("users", "r") as f:
        users = f.readlines()
        yield from set(users)


async def send_message(user_id: int, text: str, disable_notification: bool = False) -> bool:
    """
    Safe messages sender

    :param user_id:
    :param text:
    :param disable_notification:
    :return:
    """
    try:
        await bot.send_message(user_id, text, disable_notification=disable_notification)
    except exceptions.BotBlocked:
        log.error(f"Target [ID:{user_id}]: blocked by user")
    except exceptions.ChatNotFound:
        log.error(f"Target [ID:{user_id}]: invalid user ID")
    except exceptions.RetryAfter as e:
        log.error(f"Target [ID:{user_id}]: Flood limit is exceeded. Sleep {e.timeout} seconds.")
        await asyncio.sleep(e.timeout)
        return await send_message(user_id, text)  # Recursive call
    except exceptions.UserDeactivated:
        log.error(f"Target [ID:{user_id}]: user is deactivated")
    except exceptions.TelegramAPIError:
        log.exception(f"Target [ID:{user_id}]: failed")
    else:
        log.info(f"Target [ID:{user_id}]: success")
        return True
    return False


async def broadcaster() -> int:
    count = 0
    try:
        for user_id in get_users():
            with open("need_broadcast", "r") as f:
                for raw_apartment in f:
                    apartment = ujson.loads(raw_apartment)
                    apartment_message = Template(templates.single_apartment).safe_substitute(
                        rooms_count=get_rent_type(apartment["rent_type"]),
                        price_usd=apartment["price"]["converted"]["USD"]["amount"],
                        address=apartment["location"]["address"] or apartment["location"]["user_address"],
                        photo=apartment["photo"],
                    )
                    if await send_message(user_id, apartment_message):
                        count += 1
                    await asyncio.sleep(0.05)  # 20 messages per second (Limit: 30 messages per second)
    finally:
        log.info(f"{count} messages successful sent.")

    return count


if __name__ == "__main__":
    # Execute broadcaster
    executor.start(dp, broadcaster())
