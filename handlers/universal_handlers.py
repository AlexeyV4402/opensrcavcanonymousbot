from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from keyboards.builders import main_menu
from utils.lang import _
from utils.filters import IsInSQLColumn

universal_router = Router()


@universal_router.message(IsInSQLColumn("lang", "cancel"))
async def cancel(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    kb = await main_menu(message.from_user.language_code, message.from_user.id)
    await message.answer(await _("cancel", message.from_user.language_code))
    return await message.answer(
        text=await _('start', message.from_user.language_code),
        reply_markup=kb,
        parse_mode="Markdown"
    )
