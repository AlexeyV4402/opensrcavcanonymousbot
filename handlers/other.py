from aiogram import types
from aiogram import Router
from aiogram.filters import Command, CommandObject, CommandStart, StateFilter

from aiogram.fsm.context import FSMContext
from utils.statements import Start

from keyboards.builders import build_custom_from_codes
from utils.lang import _, get_code

from database.sqlite_db import sql_add_command, sql_read

other_router = Router()


@other_router.message(CommandStart(), StateFilter(None))
async def start(message: types.Message, state: FSMContext):
    if not message.chat.type == "private":
        return
    text0 = await _('0', message.from_user.language_code)
    entry = await sql_read(
        "users",
        "id",
        message.from_user.id
    )
    if entry:
        kb = await build_custom_from_codes(message.from_user.language_code, "3 4 5 6")
        return await message.answer(text=text0, reply_markup=kb)
    text1 = await _('1', message.from_user.language_code)
    await state.set_state(Start.Age)
    await message.answer(text0)
    await message.answer(text1)


@other_router.message()
async def select_service(message: types.Message):
    if not message.chat.type == "private":
        return
    word_code = get_code(message.text, message.from_user.language_code)
    if not word_code:
        return

    if word_code == "3":
        kb = await build_custom_from_codes(str(message.from_user.id), "17")
        await message.answer(await _("18", str(message.from_user.language_code)), kb=kb)

    elif word_code == "4":
        data = await sql_read(
            "users",
            "id",
            message.from_user.id
        )
        if not data:
            error_message = await _('13', message.from_user.language_code)
            return await message.answer(text=error_message.format("1"))
        else:
            out = await _('14', message.from_user.language_code)
            return await message.answer(
                text=out.format(
                    message.from_user.id,
                    data[1],    # Возраст
                    data[3],    # Приглашено
                    data[4],    # Карма
                    data[2]     # PREMIUM
                )
            )
    elif word_code == "5":
        text = await _('2', message.from_user.language_code)
        await message.answer(text=text, parse_mode="Markdown")

    elif word_code == "15":
        text = await _('16', message.from_user.language_code)
        await message.answer(text=text, parse_mode="Markdown")
