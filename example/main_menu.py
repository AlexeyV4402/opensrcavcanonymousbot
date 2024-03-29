from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from config import get_command


async def new(is_admin: bool = False):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = KeyboardButton("Пассажир")
    button2 = KeyboardButton("Водитель")
    button3 = KeyboardButton(f"/{get_command('post_service_ad')}")
    button4 = KeyboardButton(f"/{get_command('post_service_query')}")
    markup.add(button1, button2)
    markup.add(button3, button4)
    if is_admin:
        markup.row(KeyboardButton("Администратор"))
    return markup
