from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile, CallbackQuery
from bot.user.actions import get_user, create_user
from bot.user.models import User
from bot.database import create_connection
from bot.keyboards.for_questions_keyboard import (
    get_yes_kb,
    get_successful,
    get_registration_successful_kb,
    get_info_inline_kb,
)
from bot.templates_env import jinja_env
from bot.user_status import UserStatus

router = Router()


@router.message(Command("start"))
async def send_msg(message: Message):
    template = jinja_env.get_template("send_msg.txt")
    text = template.render(username=message.from_user.username)

    async with create_connection() as conn:
        user = await get_user(conn, tg_user_id=str(message.from_user.id))
        if user is None:
            await create_user(
                conn,
                User(
                    tg_user_id=str(message.from_user.id),
                    status=UserStatus.INIT,
                    chat_id=str(message.chat.id),
                ),
            )

    await message.answer(text, reply_markup=get_yes_kb())


@router.message(F.text.lower() == "да, готов✅")
async def answer_yes(message: Message):
    template = jinja_env.get_template("answer_yes.txt")
    text = template.render()

    with open("src/bot/images/promo1.jpg", "rb") as image_from_buffer:
        await message.answer_photo(
            BufferedInputFile(
                image_from_buffer.read(), filename="image from buffer.jpg"
            ),
            caption=text,
            reply_markup=get_info_inline_kb(message.from_user.id),
        )


@router.callback_query(F.data.startswith("registered"))
async def registration_successful(call: CallbackQuery):
    templates = jinja_env.get_template("registration_successful.txt")
    text = templates.render()

    async with create_connection() as conn:
        user = await get_user(conn, tg_user_id=str(call.from_user.id))

        if user is None:
            await create_user(
                conn,
                User(
                    tg_user_id=str(call.from_user.id),
                    status=UserStatus.INIT,
                    chat_id=str(call.message.chat.id),
                ),
            )
            await call.message.answer("Пожалуйста пройдите регистрацию!")
            return

    if user.status not in (UserStatus.REGISTERED, UserStatus.MADE_DEPOSIT):
        await call.message.answer("Пожалуйста пройдите регистрацию!")
        return

    await call.message.answer(text, reply_markup=get_registration_successful_kb())


@router.callback_query(F.data.startswith("made_deposit"))
async def successful(call: CallbackQuery):
    async with create_connection() as conn:
        user = await get_user(conn, tg_user_id=str(call.from_user.id))

        if user is None:
            await create_user(
                conn,
                User(
                    tg_user_id=str(call.from_user.id),
                    status=UserStatus.INIT,
                    chat_id=str(call.message.chat.id),
                ),
            )
            await call.message.answer("Пожалуйста пройдите регистрацию!")
            return

    if user.status != UserStatus.MADE_DEPOSIT:
        await call.message.answer("Пожалуйста, сделайте депозит!")
        return

    templates = jinja_env.get_template("successful.txt")
    text = templates.render()

    await call.message.answer(text, reply_markup=get_successful())
