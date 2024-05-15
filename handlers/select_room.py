from aiogram import types
from aiogram import Router
from aiogram.filters import StateFilter

from aiogram.fsm.context import FSMContext
from utils.statements import SelectRoom

from keyboards.builders import room_list, gender_list

from loader import bot

from utils.lang import _

from asyncio import run

from database.sqlite_db import sql_read, sql_add_command, sql_remove, sql_update

select_room_router = Router()


# @select_room_router.callback_query(StateFilter(SelectRoom.Region))
# async def select_region(callback: types.CallbackQuery, state: FSMContext):
#     pass


@select_room_router.callback_query(StateFilter(SelectRoom.Room))
async def select_room(callback: types.CallbackQuery, state: FSMContext):
    if "room:" in callback.data:
        await state.update_data(
            user_id=callback.from_user.id,
            region=callback.from_user.language_code,
            room_id=callback.data.split(":")[1]
        )
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=await _("select_gender", "ru"),
            reply_markup=await gender_list(callback.from_user.language_code)
        )
        await callback.answer()
        await state.set_state(SelectRoom.Gender)
    elif "room_set_page" in callback.data:
        need_page = int(callback.data.removeprefix("room_set_page:"))
        data = await sql_read(
            "users",
            "id",
            callback.from_user.id
        )
        keyboard = await room_list(
            region=callback.from_user.language_code,
            lang=callback.from_user.language_code,
            criteria_data={"age": data[0][1]},
            page=need_page
        )
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id,
            text=await _("select_room", "ru"),
            reply_markup=keyboard
        )


@select_room_router.callback_query(StateFilter(SelectRoom.Gender))
async def select_gender(callback: types.CallbackQuery, state: FSMContext):
    if not await search_interlocutor({
        "lang": callback.from_user.language_code,
        "gender": callback.data,
        "message_id": callback.message.message_id,
        "chat_id": callback.message.chat.id,
        "user_id": callback.from_user.id,
        "data": await state.get_data()
    }):
        data = await sql_read("users", "id", callback.from_user.id)
        await state.update_data(gender=callback.data, age=data[0][1])
        data = await state.get_data()
        await sql_add_command("active_queue", data)

    await callback.answer()
    await state.clear()


async def search_interlocutor(gdata):
    queue = await sql_read("active_queue", "room_id", gdata['data']['room_id'])
    queue_ = []
    for i in queue:
        partner_data = await sql_read("users", "id", i[0])
        if gdata['gender'] in [partner_data[0][6], "any"]:
            queue_.append(i)
    queue = queue_
    await sql_update(
        "users",
        "id",
        gdata['user_id'],
        "last_chat",
        f"{gdata['data']['room_id']}:{gdata['gender']}"
    )
    if len(queue):
        for i in queue:
            if i[0] == gdata['user_id']:
                return
        queue.sort(key=lambda x: x[4])
        data = await sql_read("users", "id", gdata['user_id'])
        for i in range(len(queue)):
            if queue[i][4] - 2 <= data[0][1] <= queue[i][4] + 2:
                a = queue[i]
                queue.pop(i)
                queue.insert(0, a)
        await bot.delete_message(
            chat_id=gdata['chat_id'],
            message_id=gdata['message_id']
        )
        await bot.send_message(
            chat_id=queue[0][0],
            text=await _("interlocutor_searched", gdata['lang']),
        )
        await bot.send_message(
            chat_id=gdata['user_id'],
            text=await _("interlocutor_searched", gdata['lang']),
        )
        await sql_remove("active_queue", "user_id", queue[0][0])
        await sql_add_command("active_chats", {"user_id_1": queue[0][0], "user_id_2": gdata['user_id']})
        return True
    else:
        await bot.send_message(
            chat_id=gdata['chat_id'],
            text=await _("interlocutor_searching", gdata['lang']),
        )
        return False
