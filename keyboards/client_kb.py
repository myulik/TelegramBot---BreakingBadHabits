from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
# ReplyKeyboardRemove - удаление клавиатуры

b1 = KeyboardButton('/motivate')
b2 = KeyboardButton('/active')
b3 = KeyboardButton('/info')
b4 = KeyboardButton('/log')
b5 = KeyboardButton('/new')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_client.row(b1, b2, b3, b4, b5)