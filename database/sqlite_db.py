import sqlite3 as sq


async def sql_start():
    global base, cur
    base = sq.connect('data.db')
    cur = base.cursor()
    if base:
        pass


async def sql_add_command(table: str, data):
    length = len(data)
    if type(data) == dict:
        values = data.values()
    else:
        values = data
    cur.execute(f"INSERT INTO '{table}' VALUES ({str('?, ' * length).removesuffix(', ')})", tuple(values))
    # else:
    #     async with state.proxy() as data:
    #         cur.execute(f"INSERT INTO '{table}' VALUES ({str('?, '*length).removesuffix(', ')})", tuple(state.values()))
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


async def sql_remove(table: str, key, value):
    cur.execute(f"DELETE FROM {table} WHERE {key}='{value}';")
    base.commit()


async def sql_update(table: str, key, value, replace_data_key, replace_data_value):
    cur.execute(f"UPDATE '{table}' set {replace_data_key} = '{replace_data_value}' WHERE {key}='{value}'")
    base.commit()


async def sql_table_length(table: str):
    return cur.execute(f"SELECT COUNT() FROM {table}").fetchone()[0]