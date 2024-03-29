from aiogram import types
from aiogram import Router
from aiogram.fsm.context import FSMContext
from keyboards.builders import build_custom_from_codes
from utils.lang import get_code, _

universal_router = Router()


@universal_router.message()
async def handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    word_code = get_code(message.text, message.from_user.language_code)
    if not word_code:
        return
    if word_code == "6":
        return await message.answer(
            text=await _("8", message.from_user.language_code)
        )
    elif word_code == "7":
        if current_state is None:
            return
        await state.clear()
        kb = await build_custom_from_codes(message.from_user.language_code, "3456")
        return await message.answer(
            text=await _("7", message.from_user.language_code),
            reply_markup=kb
        )
