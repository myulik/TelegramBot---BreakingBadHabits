from aiogram.types import Message, CallbackQuery
from aiogram import Dispatcher
import time
import sqlite3 as sq
from keyboards.inlinekeyb import inkcon, inkrepeat, inkfail
from aiogram.dispatcher.filters import Text
from keyboards.client_kb import kb_client
from levels import levels


async def start_bbh(message: Message):
    await message.answer(text='/active - оставшиеся время\n/info - интересная информация,\
касаемо вашей привычки, да и вообще зависимости от чего-либо\n/motivate - мотививация, когда особенно тяжело\n/log - \
завершенные уровни\n/new - новый отказ от привычки', reply_markup=kb_client)


async def active(message: Message):
    with sq.connect('BBH.db') as base:
        cur = base.cursor()
        cur.execute(f"SELECT habit, duraction, start_seconds, status FROM users WHERE user_id = {message.from_user.id}")
        daties = cur.fetchall()

        text = ''
        for data in daties:
            seconds_end = data[2] + (data[1] * 24 * 60 * 60)
            a = seconds_end - time.time()
            if data[3] == 'ACTIVE':
                if a > 0:
                    day = a // (24 * 60 * 60)
                    hour = (a % (24 * 60 * 60)) // 3600
                    minute = ((a % (24 * 60 * 60)) % 3600) // 60
                    seconds = (((a % (24 * 60 * 60)) % 3600) % 60)
                    text = f'Без  ❌{data[0]}❌  ⏳{int(day)}:{int(hour)}:{int(minute)}:{int(seconds)}'
                    await message.answer(text=text, reply_markup=inkfail)
                else:
                    text = f'⌛️Время отказа от {data[0]} истекло!'
                    cur.execute("UPDATE users SET status = ? WHERE user_id = ? AND \
                    habit = ?", ['COMPLETED', message.from_user.id, data[0]])
                    await message.answer(text=text, reply_markup=inkcon)

    if not text:
        await message.answer(text='Активных таймеров отказа пока нет.')


async def call_continuous(callback: CallbackQuery):
    await callback.answer(cache_time=30)
    with sq.connect('BBH.db') as base:
        cur = base.cursor()
        cur.execute(f"SELECT * FROM users WHERE user_id = ? AND status = ? AND \
        past = ?", [callback['from']['id'], 'COMPLETED', 'NO'])
        data = cur.fetchone()
        cur.execute("UPDATE users SET past = ? WHERE user_id = ? AND \
        habit = ? AND status = ? AND past = ?", ['YES', callback['from']['id'], data[1], 'COMPLETED', 'NO'])

        if levels[8] != data[2]:
            for i in levels:
                if levels[i] == data[2]:
                    new_dur = levels[i + 1]
                    break
            cur.execute(f'INSERT INTO users (user_id, habit, duraction, start_seconds, status, past) VALUES \
                        (?, ?, ?, ?, ?, ?)', [data[0], data[1], new_dur, time.time(), 'ACTIVE', 'NO'])
            await callback.answer(text='Отсчёт пошел', cache_time=30)
        else:
            await callback.answer(text='Вы молодцы! Все уровни выполнены!', show_alert=True)


async def call_failed(callback: CallbackQuery):
    await callback.answer(cache_time=30)
    await callback.answer(text='Отсчёт пошел', cache_time=30)
    # закончить


async def call_repeat(callback: CallbackQuery):
    await callback.answer(cache_time=30)
    await callback.answer(text='Отсчёт пошел', cache_time=30)
    # закончить


async def log(message: Message):
    with sq.connect('BBH.db') as base:
        cur = base.cursor()
        cur.execute(f"SELECT habit, duraction, start_seconds, status, past \
        FROM users WHERE user_id = ? AND (status = ? OR status = ?)", [message.from_user.id, 'COMPLETED', 'FAILED'])
        daties = cur.fetchall()

    sorted(daties, key=lambda x: x[2])

    text = ''
    for data in daties:
        seconds_end = data[2] + (data[1] * 24 * 60 * 60)
        time_string1 = time.strftime("%d/%m/%Y, %H:%M:%S", time.localtime(data[2]))
        time_string2 = time.strftime("%d/%m/%Y, %H:%M:%S", time.localtime(seconds_end))
        if data[3] == 'COMPLETED':
            text = f'{data[0]}\n\n{time_string1} - {time_string2}\n\nСтатус - ✅{data[3]}'
            if data[4] == 'NO':
                await message.answer(text=text, reply_markup=inkcon)
            else:
                await message.answer(text=text)
        else:
            text = f'{data[0]}\n\n{time_string1} - NONE\n\nСтатус - ❌{data[3]}'
            if data[4] == 'NO':
                await message.answer(text=text, reply_markup=inkrepeat)
            else:
                await message.answer(text=text)

    if not text:
        await message.answer(text='Логов пока нет.')
    # сделать инлайн кнопку для сброса всех логов


async def info(message: Message):
    pass


async def motivate(message: Message):
    await message.answer(text=':)')


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_bbh, commands=['start'])
    dp.register_message_handler(active, commands=['active'])
    dp.register_message_handler(motivate, commands=['motivate'])
    dp.register_message_handler(log, commands=['log'])
    dp.register_message_handler(info, commands=['info'])

    dp.register_callback_query_handler(call_continuous, Text(startswith='continuous'))
    dp.register_callback_query_handler(call_failed, Text(startswith='failed'))
    dp.register_callback_query_handler(call_repeat, Text(startswith='repeat'))

