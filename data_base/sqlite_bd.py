import sqlite3 as sq


def sqlite_start():
    with sq.connect('BBH.db') as base:
        cur = base.cursor()
        if base:
            print('Connecting to DataBase accomplished')
        cur.execute('CREATE TABLE IF NOT EXISTS users(user_id, \
                                    habit TEXT, duraction INTEGER, \
                                    start_seconds INTEGER, status TEXT DEFAULT ACTIVE, past TEXT DEFAULT NO)')


async def sql_add_state(state, user_id):
    async with state.proxy() as data:
        with sq.connect('BBH.db') as base:
            cur = base.cursor()
            cur.execute(f'INSERT INTO users (user_id, habit, duraction, start_seconds) VALUES {(user_id, ) + tuple(data.values())}')
