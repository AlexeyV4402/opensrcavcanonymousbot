from aiogram import types
from aiogram import Router
from aiogram.filters import Command

from loader import bot
from utils.filters import InActiveChat
from handlers.select_room import search_interlocutor

from utils.lang import _

from database.sqlite_db import sql_read, sql_remove, sql_add_command

from config import CHATS_JOURNAL

from datetime import date

import os

chat_router = Router()


@chat_router.message(Command("stop"))
async def stop(message: types.Message):
    if not message.chat.type == "private":
        return
    f = InActiveChat()
    if await f.__call__(message):
        data = await sql_read("active_chats", "user_id_1", message.from_user.id)
        if data:
            a = 0
            await sql_remove("active_chats", "user_id_1", message.from_user.id)
        else:
            data = await sql_read("active_chats", "user_id_2", message.from_user.id)
            a = 1
            await sql_remove("active_chats", "user_id_2", message.from_user.id)
        await bot.send_message(chat_id=data[0][int(a)], text=await _("dialog_closed", message.from_user.language_code))
        await bot.send_message(
            chat_id=data[0][int(not a)],
            text=await _(
                "dialog_closed_by",
                message.from_user.language_code
            )
        )
    elif await sql_read("active_queue", "user_id", message.from_user.id):
        await sql_remove("active_queue", "user_id", message.from_user.id)
        await message.answer(await _("dialog_closed", message.from_user.language_code))


@chat_router.message(InActiveChat(), Command("next"))
async def next_(message: types.Message):
    if not message.chat.type == "private":
        return
    data = await sql_read("active_chats", "user_id_1", message.from_user.id)
    if data:
        a = 0
        await sql_remove("active_chats", "user_id_1", message.from_user.id)
    else:
        data = await sql_read("active_chats", "user_id_2", message.from_user.id)
        a = 1
        await sql_remove("active_chats", "user_id_2", message.from_user.id)
    if CHATS_JOURNAL:
        filename = f"/home/AlexeyV/Data/{date.today()}/{data[0][int(a)]}-{int(not a)}.log"
        dir_name = os.path.dirname(filename)
        os.makedirs(dir_name, exist_ok=True)
        try:
            with open(filename, encoding="utf-8", mode="rt") as f:
                t = f.read()
        except FileNotFoundError:
            t = ""
        with open(filename, encoding="utf-8", mode="wt") as f:
            f.write(t + "\n" + str(message.dict()))
    await bot.send_message(chat_id=data[0][int(a)], text="❌ Вы покинули чат")
    await bot.send_message(chat_id=data[0][int(not a)], text="❌ Собеседник покинул чат")
    data = await sql_read("users", "id", message.from_user.id)
    last_chat = data[0][5].split(":")
    if not await search_interlocutor({
        "lang": message.from_user.language_code,
        "gender": last_chat[1],
        "message_id": message.message_id,
        "chat_id": message.chat.id,
        "user_id": message.from_user.id,
        "data": {
            "user_id": message.from_user.id,
            "region": message.from_user.language_code,
            "room_id": last_chat[0]
        }
    }):
        data = {
            "user_id": message.from_user.id,
            "region": message.from_user.language_code,
            "room_id": last_chat[0],
            "gender": last_chat[1],
            "age": data[0][1]
        }
        await sql_add_command("active_queue", data)


@chat_router.message(InActiveChat())
async def handler(message: types.Message):
    if not message.chat.type == "private":
        return
    data = await sql_read("active_chats", "user_id_1", message.from_user.id)
    if data:
        partner_id = data[0][1]
    else:
        data = await sql_read("active_chats", "user_id_2", message.from_user.id)
        partner_id = data[0][0]
    if message.text: await bot.send_message(chat_id=partner_id, text=message.text, protect_content=message.has_protected_content)
    if message.audio: await bot.send_audio(chat_id=partner_id, audio=message.audio, protect_content=message.has_protected_content)
    if message.photo: await bot.send_photo(chat_id=partner_id, photo=message.photo[0].file_id, protect_content=message.has_protected_content)
    if message.voice: await bot.send_voice(chat_id=partner_id, voice=message.voice, protect_content=message.has_protected_content)
    if message.video: await bot.send_video(chat_id=partner_id, video=message.video, protect_content=message.has_protected_content)
    if message.game: await bot.send_game(chat_id=partner_id, game_short_name=message.game, protect_content=message.has_protected_content)
    if message.document: await bot.send_document(chat_id=partner_id, document=message.document.file_id, protect_content=message.has_protected_content)
    if message.animation: await bot.send_animation(chat_id=partner_id, animation=message.animation.file_id, protect_content=message.has_protected_content)
    if message.sticker: await bot.send_sticker(chat_id=partner_id, sticker=message.sticker.file_id, emoji=message.sticker.emoji, protect_content=message.has_protected_content)
    if message.venue: await bot.send_venue(
        chat_id=partner_id,
        latitude=message.venue.location.latitude,
        longitude=message.venue.location.longitude,
        title=message.venue.title,
        address=message.venue.address,
        foursquare_id=message.venue.foursquare_id,
        foursquare_type=message.venue.foursquare_type,
        google_place_id=message.venue.google_place_id,
        google_place_type=message.venue.google_place_type,
        protect_content=message.has_protected_content
    )
    if message.poll: await bot.send_poll(
        chat_id=partner_id,
        question=message.poll.question,
        options=message.poll.options,
        is_anonymous=message.poll.is_anonymous,
        type=message.poll.type,
        allows_multiple_answers=message.poll.allows_multiple_answers,
        correct_option_id=message.poll.correct_option_id,
        explanation=message.poll.explanation,
        explanation_entities=message.poll.explanation_entities,
        open_period=message.poll.open_period,
        close_date=message.poll.close_date,
        is_closed=message.poll.is_closed,
        protect_content=message.has_protected_content
    )
    if message.location: await bot.send_location(
        chat_id=partner_id,
        latitude=message.location.latitude,
        longitude=message.location.longitude,
        horizontal_accuracy=message.location.horizontal_accuracy,
        live_period=message.location.live_period,
        heading=message.location.heading,
        proximity_alert_radius=message.location.proximity_alert_radius,
        protect_content=message.has_protected_content
                                                 )
    if message.contact: await bot.send_contact(
        chat_id=partner_id,
        phone_number=message.contact.phone_number,
        first_name=message.contact.first_name,
        last_name=message.contact.last_name,
        vcard=message.contact.vcard,
        protect_content=message.has_protected_content
    )
    if CHATS_JOURNAL:
        filename = f"/home/AlexeyV/Data/{date.today()}/{data[0][0]}-{partner_id}.log"
        dir_name = os.path.dirname(filename)
        os.makedirs(dir_name, exist_ok=True)
        try:
            with open(filename, encoding="utf-8", mode="rt") as f:
                t = f.read()
        except FileNotFoundError:
            t = ""
        with open(filename, encoding="utf-8", mode="wt") as f:
            f.write(t + "\n" + str(message.dict()))
