from aiogram import executor
from create_bot import dp, bot
from data_base import sqlite_bd
from create_bot import ADMIN_ID


async def send_to_admin(message):
    await bot.send_message(ADMIN_ID, 'Бот BreakingBadHabits запущен.')
    sqlite_bd.sqlite_start()


if __name__ == '__main__':
    from handlers import handlers, command_new

    handlers.register_handlers(dp)
    command_new.register_handlers_new_habit(dp)

    executor.start_polling(dp, skip_updates=True, on_startup=send_to_admin)

