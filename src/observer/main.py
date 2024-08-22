import asyncio

from aiogram import Bot

from bot.config_reader import config
from bot.database import create_connection
from bot.user.actions import get_users
from bot.user_status import UserStatus


async def main():
    bot = Bot(token=config.bot_token.get_secret_value())

    async with create_connection() as conn:
        users = await get_users(conn, status=UserStatus.INIT)

    print(users)

    for user in users:
        await bot.send_message(user.chat_id, "Зарегайся пж")

    async with create_connection() as conn:
        users = await get_users(conn, status=UserStatus.REGISTERED)

    for user in users:
        await bot.send_message(user.chat_id, "Сделай депозит пж")

    await bot.close()


if __name__ == "__main__":
    asyncio.run(main())
