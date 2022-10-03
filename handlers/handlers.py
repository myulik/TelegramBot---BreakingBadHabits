from aiogram.types import Message, CallbackQuery
from aiogram import Dispatcher
import time
from keyboards.inlinekeyb import inlExt, inlRepeat, inlFail, inlDrop
from aiogram.dispatcher.filters import Text
from keyboards.client_kb import kb_client
from data_base import sqlite_bd as bd


async def start(message: Message):
    await message.answer(text='/active - оставшиеся время\n/info - интересная информация,\
касаемо вашей привычки, да и вообще зависимости от чего-либо\n/motivate - мотививация, когда особенно тяжело\n/log - \
завершенные уровни\n/new - новый отказ от привычки', reply_markup=kb_client)
# нужно сделать меню


def time_count(dif):
    day = dif // (24 * 60 * 60)
    hour = (dif % (24 * 60 * 60)) // 3600
    minute = ((dif % (24 * 60 * 60)) % 3600) // 60
    seconds = (((dif % (24 * 60 * 60)) % 3600) % 60)
    return day, hour, minute, seconds


async def active(message: Message):
    dates = bd.get_data_active(message)
    text = ''
    for data in dates:
        user_id, habit, dur, level, sec, status = data
        dif = sec + (dur * 24 * 60 * 60) - time.time()
        if dif > 0:
            day, hour, minute, seconds = time_count(dif)
            total = dur * 24 * 60 * 60
            now = int(time.time()) - sec
            cent = (now * 100) / total
            text = f'Без {habit} ⏳{int(day)}:{int(hour)}:{int(minute)}:{int(seconds)}\n\
(Выполнено {round(cent, 3)} % из 100 %)'
            await message.answer(text=text, reply_markup=inlFail)
        else:
            await bd.update_status(message.from_user.id, habit, 'completed')
            text = f'⌛️Время отказа от {habit} истекло!'
            await message.answer(text=text, reply_markup=inlExt)
    if not text:
        await message.answer(text='Активных таймеров пока нет.')


async def call_extension(callback: CallbackQuery):
    dates = bd.get_habit(callback)
    for i in dates:
        if i[0] in callback.message.text:
            await bd.update_status(callback['from']['id'], i[0], callback.data)

    levels = {0: 1, 1: 3, 2: 7, 3: 14, 4: 21, 5: 30, 6: 90, 7: 180, 8: 365}
    user_id, habit, dur, level, sec, status = bd.get_data_extension(callback)
    if levels[8] != dur:
        for i in levels:
            if levels[i] == dur:
                new_dur = levels[i + 1]
                await bd.sql_add_state((habit, new_dur, level + 1, int(time.time())), user_id)
        await callback.answer(text='ОТСЧЁТ ПОШЁЛ', cache_time=30)
    else:
        await callback.answer(text='Вы молодцы! Все уровни выполнены!', show_alert=True, cache_time=30)


async def call_failed(callback: CallbackQuery):
    dates = bd.get_habit(callback)
    for i in dates:
        if i[0] in callback.message.text:
            await bd.update_status(callback['from']['id'], i[0], callback.data)

    await callback.answer(text='СЛАБАК')


async def call_repeat(callback: CallbackQuery):
    dates = bd.get_habit(callback)
    for i in dates:
        if i[0] in callback.message.text:
            await bd.update_status(callback['from']['id'], i[0], callback.data)

    await callback.answer(text='ОТСЧЁТ ПОШЁЛ', cache_time=30)


async def log(message: Message):
    dates = bd.get_data_log(message)

    sorted(dates, key=lambda x: x[4])

    text = ''
    for data in dates:
        user_id, habit, dur, level, sec, status = data

        time_string1 = time.strftime("%d/%m/%Y, %H:%M:%S", time.localtime(sec))
        time_string2 = time.strftime("%d/%m/%Y, %H:%M:%S", time.localtime(sec + (dur * 24 * 60 * 60)))

        if status == 'COMPLETED':
            text = f'{habit} ({level}/8)\n\n{time_string1} - {time_string2}\n\nСтатус - ✅{status} (Выполнено 100 из 100 %)'
            await message.answer(text=text, reply_markup=inlExt)
        elif status == 'FAILED':
            total = dur * 24 * 60 * 60
            now = int(time.time()) - sec
            cent = (now * 100) / total
            time_string2 = time.strftime("%d/%m/%Y, %H:%M:%S", time.localtime(time.time()))
            text = f'{habit} ({level}/8)\n\n{time_string1} - {time_string2}\n\nСтатус - ❌{status} (Выполнено {round(cent, 3)} из 100 %)'
            await message.answer(text=text, reply_markup=inlRepeat)
        else:
            text = f'{habit} ({level}/8)\n\n{time_string1} - {time_string2}\n\nСтатус - ✅{status} (Выполнено 100 из 100 %)'
            await message.answer(text=text)

    if not text:
        await message.answer(text='Логов пока нет.')


async def info(message: Message):
    await message.answer(text='В разработке')


async def motivate(message: Message):
    await message.answer(text='В разработке')


async def droplogs(message: Message):
    await message.answer(text='Вы уверены, что хотите сбросить все логи?', reply_markup=inlDrop)


async def call_droplogs(callback: CallbackQuery):
    await bd.drop_dates()
    await callback.answer(text='Данные сброшены.')


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(active, commands=['active'])
    dp.register_message_handler(motivate, commands=['motivate'])
    dp.register_message_handler(log, commands=['log'])
    dp.register_message_handler(info, commands=['info'])
    dp.register_message_handler(droplogs, commands=['droplogs'])

    dp.register_callback_query_handler(call_extension, Text(equals='completed+'))
    dp.register_callback_query_handler(call_failed, Text(equals='failed'))
    dp.register_callback_query_handler(call_repeat, Text(equals='active'))
    dp.register_callback_query_handler(call_droplogs, Text(equals='droplogs'))

