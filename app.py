from loader import dp, bot

from handlers.other import other_router
from handlers.start_questions import start_router
from handlers.universal_handlers import universal_router
from handlers.select_room import select_room_router
from handlers.anonymous_chat import chat_router

from asyncio import run, sleep
from database import sqlite_db

from utils.lang import _


async def init_sql():
    if "users" not in await sqlite_db.sql_get_tables():
        sqlite_db.sql_create_table(
            "users",
            "id INTEGER UNIQUE PRIMARY KEY",
            "age INTEGER",

            "premium INTEGER",

            "invited INTEGER",
            "karma INTEGER",

            "last_chat TEXT"
        )


async def main():
    await init_sql()
    dp.include_routers(
        other_router,
        start_router,
        select_room_router
    )
    dp.include_router(universal_router)
    dp.include_router(chat_router)

    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    run(main())
