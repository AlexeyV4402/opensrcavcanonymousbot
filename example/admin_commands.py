from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from config import get_command


async def new(is_main_admin: bool = False):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        KeyboardButton(f"X"),
        KeyboardButton(f"/{get_command('cancel')}"),
        KeyboardButton(f"/{get_command('get_my_id')}"),
        KeyboardButton(f"/{get_command('get_chat_id')}"),
        KeyboardButton(f"/{get_command('set_main_chat')}"),
        KeyboardButton(f"/{get_command('add_ettlements')}"),
        KeyboardButton(f"/{get_command('remove_ettlements')}"),
        KeyboardButton(f"/{get_command('set_post_price')}"),
        KeyboardButton(f"/{get_command('set_subscription_price')}"),
        KeyboardButton(f"/{get_command('add_drivers')}"),
        KeyboardButton(f"/{get_command('remove_drivers')}"),
        KeyboardButton(f"/{get_command('set_threads')}"),
        KeyboardButton(f"/{get_command('remove_threads')}"),
        KeyboardButton(f"/{get_command('add_service')}"),
        KeyboardButton(f"/{get_command('remove_services')}"),
        KeyboardButton(f"/{get_command('set_cooldown')}"),
        KeyboardButton(f"/{get_command('add_banned_words')}"),
        KeyboardButton(f"/{get_command('remove_banned_words')}")
    ]
    for button in buttons:
        markup.add(button)
    if is_main_admin:
        mainadmin_buttons = [
            KeyboardButton(f"/{get_command('set_active_admin')}"),
            KeyboardButton(f"/{get_command('set_tune')}"),
            KeyboardButton(f"/{get_command('edit_mode')}")
        ]
        for button in mainadmin_buttons:
            markup.add(button)
    return markup
