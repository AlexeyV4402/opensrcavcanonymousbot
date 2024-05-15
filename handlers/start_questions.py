from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from utils.statements import Start
from utils.lang import _
from database.sqlite_db import sql_add_command, sql_get_column_values
from keyboards.builders import build_custom_from_codes

start_router = Router()


@start_router.message(Start.Age)
async def set_age_handler(message: Message, state: FSMContext):
    age_str = message.text
    # if age_str in sql_get_column_values("lang", "cancel"):
    #     current_state = await state.get_state()
    #     if current_state is None:
    #         return
    #     await state.clear()
    #     return await message.answer(text=await _("cancel", "ru"))
    if not age_str.isdigit() or "." in age_str:
        return await message.answer(await _("invalid_age", message.from_user.language_code))
    age = int(age_str)
    if age >= 120:
        return await message.answer(await _("too_much_age", message.from_user.language_code))
    elif 5 < age < 120:
        await state.update_data(age=age)
        await state.set_state(Start.Gender)
        keyboard = await build_custom_from_codes("ru", "male female")
        return await message.answer(
            await _("select_own_gender", message.from_user.language_code),
            reply_markup=keyboard
        )
    elif age <= 5:
        return await message.answer(await _("too_less_age", message.from_user.language_code))


@start_router.callback_query(Start.Gender)
async def set_gender_handler(callback: CallbackQuery, state: FSMContext):
    selected = callback.data
    data = await state.get_data()
    await sql_add_command(
        "users",
        {
            "id": callback.from_user.id,
            "age": data['age'],
            "premium": 0,
            "invited": 0,
            "karma": 0,
            "last_chat": "null",
            "gender": selected
         }
    )
    await callback.answer()
    await state.clear()
    await callback.message.delete()
    return await callback.message.answer(await _("saved", callback.from_user.language_code))