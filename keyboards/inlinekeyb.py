from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


inlDur = InlineKeyboardMarkup(row_width=1)
inlDur.row(InlineKeyboardButton(text='365 дней (уровень 8)', callback_data='8level_365')).\
         row(InlineKeyboardButton(text='180 дней (уровень 7)', callback_data='7level_180')).\
         row(InlineKeyboardButton(text='90 дней (уровень 6)', callback_data='6level_90')).\
         row(InlineKeyboardButton(text='30 дней (уровень 5)', callback_data='5level_30')).\
         row(InlineKeyboardButton(text='21 день (уровень 4)', callback_data='4level_21')).\
         row(InlineKeyboardButton(text='14 дней (уровень 3)', callback_data='3level_14')).\
         row(InlineKeyboardButton(text='7 дней (уровень 2)', callback_data='2level_7')).\
         row(InlineKeyboardButton(text='3 дня (уровень 1)', callback_data='1level_3')).\
         row(InlineKeyboardButton(text='1 день (уровень 0)', callback_data='0level_1'))


inlStart = InlineKeyboardMarkup(row_width=1)
inlStart.row(InlineKeyboardButton(text="Да", callback_data='launch'),
             InlineKeyboardButton(text="Нет, сбросить данные", callback_data='exit'))


inlExt = InlineKeyboardMarkup(row_width=1)
inlExt.row(InlineKeyboardButton(text="Перейти на следующий уровень", callback_data='completed+'),
           InlineKeyboardButton(text="Повторить", callback_data='active'))


inlRepeat = InlineKeyboardMarkup(row_width=1)
inlRepeat.add(InlineKeyboardButton(text="Повторить", callback_data='active'))


inlFail = InlineKeyboardMarkup(row_width=1)
inlFail.add(InlineKeyboardButton(text="Сдаться", callback_data='failed'))

inlDrop = InlineKeyboardMarkup(row_width=1)
inlDrop.row(InlineKeyboardButton(text="Да", callback_data='droplogs'),
             InlineKeyboardButton(text="Нет, не сбрасывать данные", callback_data='nofdasfa'))
