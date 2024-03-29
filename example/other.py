from aiogram import types
from aiogram import Router
from aiogram.filters import Command, CommandObject, CommandStart, StateFilter

from keyboards.builders import main_menu
from utils.lang import _

from database.sqlite_db import sql_add_command, sql_read

other_router = Router()


@other_router.message(CommandStart(), StateFilter(None))
async def start(message: types.Message):
    if not message.chat.type == "private":
        return
    entry = await sql_read(
        ""
    )
    if not
    kb = await main_menu(message.from_user.language_code)
    text = await _('0', message.from_user.language_code)
    await sql_add_command(
        "users",
        {
            "id": message.from_user.id,
            "age": "",

            "premium": 0,

            "invited": 0,
            "karma": 0
        }
    )
    await message.answer(text=text, reply_markup=kb)


@other_router.message()
async def select_service(message: types.Message):
    if not message.chat.type == "private":
        return
    if message.text == "Открыть чат":
        pass
    elif message.text == "Правила":
        text = await _('2', message.from_user.language_code)
        await message.answer(text=text, parse_mode="Markdown")
    elif message.text == "Профиль":
        pass