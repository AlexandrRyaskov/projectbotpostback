from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.config_reader import config


def get_yes_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Да, готов✅")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def get_info_inline_kb(tg_user_id):
    inline_kb_list = [
        [InlineKeyboardButton(text="Зарегистрироваться", url=config.reg)],
        [InlineKeyboardButton(text="Я зарегестрировался", callback_data="registered")],
        [InlineKeyboardButton(text="Нужна помощь", url=config.help)],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def get_registration_successful_kb():
    inline_kb_list = [
        # [InlineKeyboardButton(text="Пополнить счет", url=config.replenishment)],
        [InlineKeyboardButton(text="Я оплатил", callback_data="made_deposit")],
        [InlineKeyboardButton(text="Нужна помощь", url=config.help)],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)


def get_successful():
    inline_kb_list = [[InlineKeyboardButton("Вступить в канал", url=config.channel)]]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
