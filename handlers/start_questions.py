from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from utils.statements import Start
from utils.lang import _
from database.sqlite_db import sql_add_command

start_router = Router()


@start_router.message(Start.Age)
async def set_name_handler(message: Message, state: FSMContext):
    age_str = message.text
    if not age_str.isdigit() or "." in age_str:
        return await message.answer(await _("9", message.from_user.language_code))
    age = int(age_str)
    if age >= 120:
        return await message.answer(await _("10", message.from_user.language_code))
    elif 5 < age < 120:
        await sql_add_command(
            "users",
            {
                "id": message.from_user.id,
                "age": age,
                "premium": 0,
                "invited": 0,
                "karma": 0,
                "last_chat": "null"
             }
        )
        await state.clear()
        return await message.answer(await _("11", message.from_user.language_code))
    elif age <= 5:
        return await message.answer(await _("12", message.from_user.language_code))
