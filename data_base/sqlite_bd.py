import sqlite3 as sq
import time


def sqlite_start():
    with sq.connect('.Base_data/BBH.db') as base:
        cur = base.cursor()
        if base:
            print('Connecting to DataBase accomplished')

        cur.execute("""CREATE TABLE IF NOT EXISTS users
        (user_id, habit TEXT, duraction
        INTEGER, level INTEGER, start_seconds INTEGER, 
        status TEXT DEFAULT ACTIVE)""")


async def sql_add_state(data, user_id):
    with sq.connect('BBH.db') as base:
        cur = base.cursor()
        cur.execute('INSERT INTO users (user_id, habit, duraction, level,\
        start_seconds) VALUES (?, ?, ?, ?, ?)', (user_id, *tuple(data)))


# получаем все записи пользователя со статусом user_id
def get_data_active(message):
    with sq.connect('BBH.db') as base:
        cur = base.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = ? AND status = ?", (message.from_user.id, "ACTIVE"))
        return cur.fetchall()


def get_data_extension(callback, habit):
    with sq.connect('BBH.db') as base:
        cur = base.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = ? AND status = ? AND \
        habit ?", [callback['from']['id'], 'COMPLETED+', habit])
        return cur.fetchone()


async def update_status(user_id, habit, callback_data):
    with sq.connect('BBH.db') as base:
        cur = base.cursor()
        if callback_data == 'failed':
            cur.execute("UPDATE users SET status = ? WHERE user_id = ? AND \
            habit = ? AND status = ?", ['FAILED', user_id, habit, 'ACTIVE'])
        elif callback_data == 'completed':
            cur.execute("UPDATE users SET status = ? WHERE user_id = ? AND \
            habit = ? AND status = ?", ['COMPLETED', user_id, habit, 'ACTIVE'])
        elif callback_data == 'completed+':
            cur.execute("UPDATE users SET status = ? WHERE user_id = ? AND \
            habit = ? AND status = ?", ['COMPLETED+', user_id, habit, 'COMPLETED'])
        elif callback_data == 'active':
            cur.execute("UPDATE users SET status = ?, start_seconds = ? WHERE user_id = ? AND \
            habit = ? AND (status = ? OR status = ?)", ['ACTIVE', int(time.time()),  user_id, habit, 'FAILED', 'COMPLETED'])


def get_data_log(message):
    with sq.connect('BBH.db') as base:
        cur = base.cursor()
        cur.execute(f"SELECT * FROM users WHERE user_id = ? \
        AND status != ?", [message.from_user.id, 'ACTIVE'])
        return cur.fetchall()


def get_habit(message):
    with sq.connect('BBH.db') as base:
        cur = base.cursor()
        cur.execute(f"SELECT habit FROM users WHERE user_id = ?", (message['from']['id'], ))
        return cur.fetchall()


async def drop_dates():
    with sq.connect('BBH.db') as base:
        cur = base.cursor()
        cur.execute("DELETE FROM users WHERE status != ?", ('ACTIVE', ))



