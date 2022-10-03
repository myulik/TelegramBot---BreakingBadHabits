from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/motivate')
b2 = KeyboardButton('/active')
b3 = KeyboardButton('/info')
b4 = KeyboardButton('/log')
b6 = KeyboardButton('/new')
b5 = KeyboardButton('/droplogs')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_client.row(b1, b2, b3).row(b4, b5, b6)