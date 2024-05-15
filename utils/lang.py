from config import TECH_SUPPORT_URL
from database.sqlite_db import *


async def get_available_languages():
    return sql_get_column_values("lang", "lang_code")


async def _(word_code: str, lang: str):
    result = await sql_get_value("lang", "lang_code", lang, word_code)
    return result[0][0]


# async def get_code(text: str, lang: str):
#     all_words = await get_all()
#     if text not in all_words:
#         return False
#     return list(translations[lang].keys())[list(translations[lang].values()).index(text)]