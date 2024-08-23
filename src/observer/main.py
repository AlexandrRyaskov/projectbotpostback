import asyncio
import logging
from aiogram import Bot
from bot.database import create_connection
from bot.keyboards.for_questions_keyboard import get_info_inline_kb
from bot.templates_env import jinja_env
from bot.user.actions import get_users
from bot.user_status import UserStatus


async def observer(bot: Bot):
    await asyncio.sleep(10)
    logging.basicConfig(level=logging.INFO)
    template = jinja_env.get_template("not_reg.txt")
    text = template.render()

    async with create_connection() as conn:
        users = await get_users(conn, status=UserStatus.INIT)

    for user in users:
        await bot.send_photo(
            user.chat_id,
            photo="src/bot/images/qqq.jpg",  # "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSx6yT7oBWFeKJH-85mTe_LX8XL5RXw1mRFow&s"
            caption=text,
            reply_markup=get_info_inline_kb(user.tg_user_id),
        )

    await observer(bot)
