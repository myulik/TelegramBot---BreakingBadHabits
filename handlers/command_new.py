from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types
from aiogram import Dispatcher
from data_base import sqlite_bd as bd
from keyboards import inlinekeyb as inl
import time


class FSMNew(StatesGroup):
    habit = State()
    duration = State()
    start = State()


# намеренный выход из машины состояний
async def cancel_handler(callback: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await callback.answer(text='Данные сброшены', cache_time=30)


async def start_new(message: types.Message):
    await message.answer("Здравствуйте, введите название привычки, от которой Вы намерены избавиться.")
    await FSMNew.habit.set()


#  state = dp.current_state(chat=message.chat.id, user=message.from_user.id)
async def load_habit(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['habit'] = message.text
    await FSMNew.next()
    await message.answer('Выберите длительность отказа от этой привычки.')
    await message.answer('*рекомендуется начать с самого нижнего уровня.', reply_markup=inl.inlDur)


async def load_duration(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer(cache_time=30)
    await FSMNew.next()
    async with state.proxy() as data:
        data['duration'] = float(callback.data.split('_')[1])
        data['level'] = int(callback.data[0])
    await callback.message.answer('Благодарю за ответы.')
    await callback.message.answer('Начать отсчет?', reply_markup=inl.inlStart)


async def start_to_countdown(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['start_seconds'] = int(time.time())
        await bd.sql_add_state(data.values(), callback['from']['id'])
    await state.finish()    # выход бота из машины состояний, словарь data очищается
    await callback.answer(text='Отсчёт пошел', cache_time=30)


def register_handlers_new_habit(dp: Dispatcher):
    dp.register_message_handler(start_new, commands=["new"], state=None)
    dp.register_message_handler(load_habit, state=FSMNew.habit)

    dp.register_callback_query_handler(load_duration, Text(contains='level'), state=FSMNew.duration)
    dp.register_callback_query_handler(cancel_handler, Text(startswith='exit'), state=FSMNew.start)
    dp.register_callback_query_handler(start_to_countdown, Text(startswith='launch'), state=FSMNew.start)





