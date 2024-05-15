from aiogram import types
from aiogram import Router
from aiogram.filters import CommandStart, StateFilter

from aiogram.fsm.context import FSMContext

from datetime import timedelta

from loader import bot

from keyboards.builders import *

from utils.lang import _
from utils.statements import Start, SelectRoom
from utils.filters import parse_criteria
from utils.time import *

from pay import *

from handlers.select_room import search_interlocutor

from database.sqlite_db import sql_read, sql_add_command, sql_update

other_router = Router()


@other_router.message(CommandStart(), StateFilter(None))
async def start(message: types.Message, state: FSMContext):
    if not message.chat.type == "private":
        return
    start_text = await _('start', message.from_user.language_code)
    entry = await sql_read(
        "users",
        "id",
        message.from_user.id
    )
    if entry:
        kb = await main_menu(
            message.from_user.language_code,
            message.from_user.id
        )
        return await message.answer(text=start_text, reply_markup=kb, parse_mode="Markdown")
    text1 = await _('select_age', message.from_user.language_code)
    await state.set_state(Start.Age)
    await message.answer(start_text)
    await message.answer(text1)


async def check_payment(user_id, region):
    variants = await sql_read("premium_prices", "region", region)
    for i in variants:
        if await check_to_payment(user_id, timedelta(minutes=60), label=str(i[5])):
            await sql_update("users", "id", user_id, "premium", time() + days_to_seconds(i[1]))
            return days_to_seconds(i[1])
    else:
        return 0


@other_router.callback_query(StateFilter(None))
async def main_menu_handler(callback: types.CallbackQuery, state: FSMContext):
    if not callback.message.chat.type == "private":
        return
    user_data = await sql_read("users", "id", callback.from_user.id)
    if not user_data:
        error_message = await _('error', callback.from_user.language_code)
        return await callback.message.answer(text=error_message.format("1"))
    premium_time = user_data[0][2]
    if premium_time - time() < 0:
        premium_time = 0
    await sql_update("users", "id", callback.from_user.id, "premium", premium_time)
    if callback.data == "last_chat":
        last_chat = user_data[0][5].split(":")
        chat = await sql_read("rooms", "id", last_chat[0])
        if not parse_criteria(chat[0][3], {
            "age": user_data[0][1],
            "premium": user_data[0][2]
        }):
            error_message = await _('error', callback.from_user.language_code)
            await callback.message.answer(text=error_message.format("2"))
            await bot.delete_message(callback.message.chat.id, callback.message.message_id)
        if not await search_interlocutor({
            "lang": callback.from_user.language_code,
            "gender": last_chat[1],
            "message_id": callback.message.message_id,
            "chat_id": callback.message.chat.id,
            "user_id": callback.from_user.id,
            "data": {
                "user_id": callback.from_user.id,
                "region": callback.from_user.language_code,
                "room_id": last_chat[0]
            }
        }):
            data = {
                "user_id": callback.from_user.id,
                "region": callback.from_user.language_code,
                "room_id": last_chat[0],
                "gender": last_chat[1],
                "age": user_data[0][1]
            }
            await sql_add_command("active_queue", data)
    elif callback.data == "select_room":
        keyboard = await room_list(
            region=callback.from_user.language_code,
            lang=callback.from_user.language_code,
            criteria_data={
                "age": user_data[0][1],
                "premium": user_data[0][2]
                           },
            page=0
        )
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=await _("select_room", "ru"),
            reply_markup=keyboard
        )
        await state.set_state(SelectRoom.Room)
    elif callback.data == "profile":
        await check_payment(callback.from_user.id, callback.from_user.language_code)
        keyboard = await build_custom_from_codes(callback.from_user.language_code, "premium")
        out = await _("profile_data", callback.from_user.language_code)
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=out.format(
                callback.from_user.id,
                (user_data[0][1] if user_data[0][1] < 32767 else "∞"),  # Возраст
                await _(user_data[0][6], callback.from_user.language_code),  # Пол
                user_data[0][3],  # Приглашено
                user_data[0][4],  # Карма
                timedelta(seconds=premium_time)-timedelta(seconds=time())   # PREMIUM
            ),
            reply_markup=keyboard
        )
    elif callback.data == "rules":
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=await _("rules_list", callback.from_user.language_code)
        )
    elif callback.data == "premium":
        keyboard = await premium_tariff(callback.from_user.language_code)
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=await _("premium_description", callback.from_user.language_code),
            parse_mode="Markdown",
            reply_markup=keyboard
        )
    elif "pay" in callback.data:
        # await callback.message.answer(await _("in_beta", callback.from_user.language_code))
        payment = callback.data.removeprefix("pay:").split(":")
        price = payment[0]
        text = payment[1]
        quickpay = create_quickpay(
            user_id=callback.from_user.id,
            label=text,
            price=int(price)
        )

        keyboard = await link_button(text=text, link=quickpay['redirected_url'])
        await callback.message.answer(
            text=text,
            reply_markup=keyboard
        )

    await callback.answer()

