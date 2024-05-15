from aiogram.filters import Filter
from aiogram.types import Message
from database.sqlite_db import sql_get_column_values, sql_read


class IsInSQLColumn(Filter):
    def __init__(self, table: str, column: str) -> None:
        self.table = table
        self.column = column

    async def __call__(self, message: Message) -> bool:
        check = [x.lower() for x in sql_get_column_values(self.table, self.column)]
        if message.text:
            return message.text.lower() in check
        else:
            return False


class InActiveChat(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: Message) -> bool:
        chats1 = await sql_read("active_chats", "user_id_1", message.from_user.id)
        chats2 = await sql_read("active_chats", "user_id_2", message.from_user.id)
        if chats1 or chats2:
            return True
        return False


def parse_criteria(criteria: str, data: dict):
    if not criteria:
        return True
    criteria = criteria.split(" ")
    for i in data:
        criteria[0] = criteria[0].replace('{'+i+'}', str(data[i]))
    if criteria[1] == ">=":
        if float(criteria[0]) >= float(criteria[2]):
            return True
    elif criteria[1] == ">":
        if float(criteria[0]) > float(criteria[2]):
            return True
    return False
