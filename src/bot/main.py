import asyncio
import logging
from aiogram import Bot, Dispatcher
from config_reader import config
from handlers import questions
from observer.main import observer


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()

    dp.include_routers(questions.router)

    await bot.delete_webhook(drop_pending_updates=True)

    task2 = asyncio.create_task(observer(bot))
    await dp.start_polling(bot)
