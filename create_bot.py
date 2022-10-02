from config import config
from aiogram import Bot, Dispatcher    # Bot - it's class, Dispatcher - доставщик update, executor - для запуска бота
import asyncio
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
loop = asyncio.get_event_loop()    # поток, в котором будут обрабатываться все события

bot = Bot(config.bot_token.get_secret_value())    # передаём токен и создает объект класса Bot
dp = Dispatcher(bot, loop=loop, storage=storage)    # обработчик и доставщик