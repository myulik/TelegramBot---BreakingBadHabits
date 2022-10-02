from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types
from main import dp
from aiogram import Dispatcher
from data_base import sqlite_bd
from keyboards import inlinekeyb as inl
import time


class FSMAdmin(StatesGroup):
    habit = State()
    duration = State()
    start = State()


# намеренный выход из машины состояний
async def cancel_handler(callback: types.CallbackQuery):
    state = dp.current_state(chat=callback.from_user.id, user=callback['from']['id'])
    await state.finish()
    await callback.answer(text='Данные сброшены', cache_time=30)


async def start_new(message: types.Message):
    await message.answer("Здравствуйте, введите название привычке, от которой Вы намерены избавиться.")
    await FSMAdmin.habit.set()


async def load_habit(message: types.Message):
    state = dp.current_state(chat=message.chat.id, user=message.from_user.id)
    async with state.proxy() as data:
        data['habit'] = message.text
    await FSMAdmin.next()
    await message.answer('Выберите длительность отказа от этой привычки.')
    await message.answer('*рекомендуется начать с самого нижнего уровня.', reply_markup=inl.inkb)


async def load_duration(callback: types.CallbackQuery):
    state = dp.current_state(chat=callback.from_user.id, user=callback['from']['id'])
    await callback.answer(cache_time=30)
    await FSMAdmin.next()
    async with state.proxy() as data:
        data['duration'] = float(callback.data.split('_')[1])
    await callback.message.answer('Благодарю за ответы.')
    await callback.message.answer('Начать отсчет?', reply_markup=inl.inks)


async def start_to_countdown(callback: types.CallbackQuery):
    state = dp.current_state(chat=callback.from_user.id, user=callback['from']['id'])
    await callback.answer(text='Отсчёт пошел', cache_time=30)
    async with state.proxy() as data:
        data['start_seconds'] = int(time.time())
    await sqlite_bd.sql_add_state(state, callback['from']['id'])
    await state.finish()    # выход бота из машины состояний, словарь data очищается


def register_handlers_new_habit(dp: Dispatcher):
    dp.register_message_handler(start_new, commands=["new"], state=None)
    dp.register_message_handler(load_habit, state=FSMAdmin.habit)
    dp.register_callback_query_handler(load_duration, Text(startswith='level'), state=FSMAdmin.duration)
    dp.register_callback_query_handler(cancel_handler, Text(startswith='отмена'), state=FSMAdmin.start)
    dp.register_callback_query_handler(start_to_countdown, Text(startswith='начало'), state=FSMAdmin.start)





