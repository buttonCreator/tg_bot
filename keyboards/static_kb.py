from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


b1 = KeyboardButton('Информация по картам')
b2 = KeyboardButton('Раздел \"Кредиты\"')
b3 = KeyboardButton('Контакты для связи с банком')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_client.add(b1, b2, b3)

