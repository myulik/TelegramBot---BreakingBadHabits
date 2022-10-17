from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/active')
b2 = KeyboardButton('/log')
b3 = KeyboardButton('/new')
b4 = KeyboardButton('/droplogs')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_client.row(b1, b2, b3).row(b4)