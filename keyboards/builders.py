from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from utils.lang import _


async def build_custom_from_codes(lang: str, include: str):
    builder = ReplyKeyboardBuilder()
    [builder.button(text=await _(item, lang)) for item in include.split(" ")]
    builder.adjust(1)
    return builder.as_markup(
        resize_keyboard=True,
        selective=True
    )


async def build_custom(buttons: str):
    builder = ReplyKeyboardBuilder()
    [builder.button(text=item) for item in buttons]
    builder.adjust(2)
    return builder.as_markup(
        resize_keyboard=True,
        selective=True
    )


async def premium_tariff():
    builder = InlineKeyboardBuilder()
    buttons = [
        ["7 days (139 ₽)", "7"],
        ["1 month (499 ₽)", "31"],
        ["6 month (2399 ₽)", "186"],
        ["1 year (4399 ₽)", "366"]
    ]
    [builder.button(text=item[0], callback_data=item[1]) for item in buttons]
    builder.adjust(1)
    return builder.as_markup(
        resize_keyboard=True,
        selective=True
    )
