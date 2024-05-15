import sqlite3
import sqlite3 as sq


base = sq.connect('/home/AlexeyV/Documents/Python/Telegram Bots/AnonymousBot/data.db')
cur = base.cursor()


async def sql_add_command(table: str, data):
    length = len(data)
    if type(data) == dict:
        values = data.values()
    else:
        values = data
    cur.execute(f"INSERT INTO '{table}' VALUES ({str('?, ' * length).removesuffix(', ')})", tuple(values))
    base.commit()


def sql_create_table(name: str, *columns):
    columns_ = ", ".join(columns)         # example: id TEXT PRIMARY KEY, sub_time TEXT
    if not columns_:
        return
    base.execute(
     f"""CREATE TABLE IF NOT EXISTS '{name}'({columns_})"""
    )
    base.commit()


async def sql_get_tables():
    return cur.execute("""SELECT name FROM sqlite_master WHERE type='table';""").fetchall()


async def sql_read(table: str, key, value=None):
    if key == "*":
        return cur.execute(f"SELECT * FROM '{table}';").fetchall()
    else:
        return cur.execute(f"SELECT * FROM '{table}' WHERE {key} = '{value}';").fetchall()


async def sql_get_value(table: str, check_key, check_value, output_key):
    return cur.execute(f"SELECT {output_key} FROM '{table}' WHERE {check_key} = '{check_value}';").fetchall()


async def sql_remove(table: str, key, value):
    cur.execute(f"DELETE FROM {table} WHERE {key}='{value}';")
    base.commit()


async def sql_update(table: str, key, value, replace_data_key, replace_data_value):
    cur.execute(f"UPDATE '{table}' set {replace_data_key} = '{replace_data_value}' WHERE {key}='{value}'")
    base.commit()


async def sql_table_length(table: str):
    return cur.execute(f"SELECT COUNT() FROM {table}").fetchone()[0]


def sql_get_column_values(table: str, column: str):
    global cur
    data = cur.execute(f"SELECT {column}, {column} FROM {table}").fetchall()
    return [str(i[0]).lower() for i in data]