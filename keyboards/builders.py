from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, InlineKeyboardMarkup
from utils.lang import _
from utils.filters import parse_criteria
from database.sqlite_db import sql_read


async def build_custom_from_codes(lang: str, include: str):
    builder = InlineKeyboardBuilder()
    [builder.button(text=await _(item, lang), callback_data=item) for item in include.split(" ")]
    builder.adjust(1)
    return builder.as_markup(
        resize_keyboard=True,
        selective=True
    )


async def build_custom(buttons):
    builder = InlineKeyboardBuilder()
    builder.add(*buttons)
    builder.adjust(1)
    return builder.as_markup(
        resize_keyboard=True,
        selective=True
    )


async def main_menu(lang: str, user_id: int):
    entry = await sql_read("users", "id", user_id)
    buttons_codes = ["select_room", "profile", "rules"]
    if entry[0][5] != 'null':
        buttons_codes.insert(0, "last_chat")
    buttons = [InlineKeyboardButton(text=await _(item, lang), callback_data=item) for item in buttons_codes]
    kb = await build_custom(buttons)
    return kb


async def room_list(region: str, lang: str, criteria_data: dict, page: int = 0):
    rooms = [x for x in await sql_read("rooms", "region", region) if parse_criteria(x[3], data=criteria_data)]
    return await create_keyboard_from_list_in_list(
        data_list=rooms,
        height=4,
        call_data="room",
        page=page
    )


async def gender_list(lang: str):
    return await build_custom_from_codes(lang, "male female any")


async def premium_tariff(region: str):
    buttons = await sql_read("premium_prices", "region", region)
    return await build_custom([InlineKeyboardButton(text=i[4], callback_data=f"pay:{i[3]}:{i[4]}") for i in buttons])


async def link_button(text: str, link: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=text, url=link)
            ]
        ],
        resize_keyboard=True,
        selective=True
    )


async def create_keyboard_from_list_in_list(data_list: list, height: int, call_data: str, page: int = 0):
    index = page * 4
    buttons = []
    for button in range(len(data_list) - page * 4):
        if index < page * 4 + 4:
            try:
                buttons.append(InlineKeyboardButton(
                    text=str(data_list[index][2]),
                    callback_data=f"{call_data}:{data_list[index][0]}")
                )
                #print(f"{call_data}:{data_list[index][in_list_index]}")
            except IndexError:
                pass
            index += 1
        else:
            break
    if index < len(data_list):
        buttons.append(InlineKeyboardButton(text=">>>", callback_data=f"{call_data}_set_page:{page + 1}"))
    if index > height:
        buttons.append(InlineKeyboardButton(text="<<<", callback_data=f"{call_data}_set_page:{page - 1}"))
    return await build_custom(buttons)
