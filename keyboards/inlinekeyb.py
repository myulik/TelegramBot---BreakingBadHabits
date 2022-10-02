from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


inkb = InlineKeyboardMarkup(row_width=1)

inkb.row(InlineKeyboardButton(text='365 дней (уровень 8)', callback_data='level_365')).\
         row(InlineKeyboardButton(text='180 дней (уровень 7)', callback_data='level_180')).\
         row(InlineKeyboardButton(text='90 дней (уровень 6)', callback_data='level_90'))

inkb.row(InlineKeyboardButton(text='30 дней (уровень 5)', callback_data='level_30')).\
         row(InlineKeyboardButton(text='21 день (уровень 4)', callback_data='level_21')).\
         row(InlineKeyboardButton(text='14 дней (уровень 3)', callback_data='level_14'))

inkb.row(InlineKeyboardButton(text='7 дней (уровень 2)', callback_data='level_7')).\
         row(InlineKeyboardButton(text='3 дня (уровень 1)', callback_data='level_3')).\
         row(InlineKeyboardButton(text='1 день (уровень 0)', callback_data='level_1'))


inks = InlineKeyboardMarkup(row_width=1).row(InlineKeyboardButton(text="Да", callback_data='начало'),
                                             InlineKeyboardButton(text="Нет, сбросить данные", callback_data='отмена'))


inkcon = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text="Перейти на следующий уровень", callback_data='continuous'))


inkrepeat = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text="Повторить", callback_data='repeat'))

inkfail = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text="Сдаться", callback_data='failed'))

