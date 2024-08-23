import asyncio
import logging
from aiogram import Bot, Dispatcher
from bot.config_reader import config
from bot.database import create_connection
from bot.handlers import questions
from observer.main import observer


async def main():
    async with create_connection() as conn:
        cur = await conn.cursor()
        await cur.execute(
            """
            CREATE TABLE public.users (
                id serial4 NOT NULL,
                tg_user_id varchar NOT NULL,
                win_user_id varchar NULL,
                status varchar NOT NULL,
                chat_id varchar NOT NULL,
                CONSTRAINT users_pkey PRIMARY KEY (id)
            );
            """
        )

    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()

    dp.include_routers(questions.router)

    await bot.delete_webhook(drop_pending_updates=True)

    task2 = asyncio.create_task(observer(bot))
    await dp.start_polling(bot)
