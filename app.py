from loader import dp, bot

from handlers.other import other_router
from handlers.start_questions import start_router
from handlers.universal_handlers import universal_router

from asyncio import run
from database.sqlite_db import sql_start, sql_get_tables, sql_create_table


async def init_sql():
    await sql_start()
    if "users" not in await sql_get_tables():
        sql_create_table(
            "users",
            "id INTEGER UNIQUE PRIMARY KEY",
            "age INTEGER",

            "premium INTEGER",

            "invited INTEGER",
            "karma INTEGER",

            "last_chat TEXT"
        )


async def main():
    dp.include_routers(
        other_router,
        start_router
    )

    dp.include_router(universal_router)
    await init_sql()
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    run(main())
