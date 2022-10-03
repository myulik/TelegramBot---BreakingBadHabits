import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
import asyncio
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging

# logging.basicConfig(format=u'%(filename)s [LINE:%(1ineno)d] #%(levelname)-8s [%(asctime)s] %(message)s',
#                     level=logging.INFO)

load_dotenv()    # помогает достать переменные из .env

TOKEN = os.getenv('TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')


storage = MemoryStorage()
loop = asyncio.get_event_loop()    # поток, в котором будут обрабатываться все события

bot = Bot(token=TOKEN, parse_mode='HTML')    # передаём токен и создает объект класса Bot
dp = Dispatcher(bot, loop=loop, storage=storage)    # обработчик и доставщик