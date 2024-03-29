from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from config import get_command


async def new():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        KeyboardButton(f"/{get_command('cancel')}"),
        KeyboardButton(f"/{get_command('start')}"),
        KeyboardButton(f"/{get_command('post_query_driver')}"),
        KeyboardButton(f"/{get_command('find_driver')}"),
        KeyboardButton(f"/{get_command('help_command')}")
    ]
    for button in buttons:
        markup.add(button)
    return markup
